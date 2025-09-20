-- Skill Tree Survey Database Schema
-- Generated from SQLAlchemy models
-- Database: SQLite

-- ============================================
-- Questions Table (Self-referencing for tree structure)
-- ============================================
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER,
    text TEXT NOT NULL,
    is_base BOOLEAN NOT NULL DEFAULT 0,
    category VARCHAR(50),
    order_index INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,

    FOREIGN KEY (parent_id) REFERENCES questions(id) ON DELETE CASCADE
);

-- Indexes for questions
CREATE INDEX ix_questions_parent_id ON questions(parent_id);
CREATE INDEX ix_questions_category ON questions(category);
CREATE INDEX ix_questions_is_base ON questions(is_base);
CREATE INDEX ix_questions_order_index ON questions(order_index);

-- ============================================
-- Survey Sessions Table
-- ============================================
CREATE TABLE survey_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name VARCHAR(100) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Indexes for survey_sessions
CREATE INDEX ix_survey_sessions_user_email ON survey_sessions(user_email);
CREATE INDEX ix_survey_sessions_company ON survey_sessions(company);
CREATE INDEX ix_survey_sessions_completed_at ON survey_sessions(completed_at);

-- ============================================
-- Responses Table
-- ============================================
CREATE TABLE responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    answer BOOLEAN NOT NULL,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id) REFERENCES survey_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    UNIQUE (session_id, question_id)
);

-- Indexes for responses
CREATE INDEX ix_responses_session_id ON responses(session_id);
CREATE INDEX ix_responses_question_id ON responses(question_id);
CREATE INDEX ix_responses_answer ON responses(answer);

-- ============================================
-- Category Orders Table (for display ordering)
-- ============================================
CREATE TABLE category_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category VARCHAR(50) UNIQUE NOT NULL,
    order_index INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for category_orders
CREATE INDEX ix_category_orders_category ON category_orders(category);
CREATE INDEX ix_category_orders_order_index ON category_orders(order_index);

-- ============================================
-- Sample Data Queries
-- ============================================

-- Get all base questions ordered
SELECT * FROM questions
WHERE is_base = 1
ORDER BY order_index;

-- Get child questions for a parent
SELECT * FROM questions
WHERE parent_id = ?
ORDER BY order_index;

-- Get session with response count
SELECT
    s.*,
    COUNT(r.id) as response_count,
    SUM(CASE WHEN r.answer = 1 THEN 1 ELSE 0 END) as yes_count
FROM survey_sessions s
LEFT JOIN responses r ON s.id = r.session_id
GROUP BY s.id;

-- Get category statistics for a session
SELECT
    q.category,
    COUNT(r.id) as total_questions,
    SUM(CASE WHEN r.answer = 1 THEN 1 ELSE 0 END) as yes_count,
    ROUND(100.0 * SUM(CASE WHEN r.answer = 1 THEN 1 ELSE 0 END) / COUNT(r.id), 2) as percentage_yes
FROM responses r
JOIN questions q ON r.question_id = q.id
WHERE r.session_id = ? AND q.category IS NOT NULL
GROUP BY q.category;

-- Get question tree with depth
WITH RECURSIVE question_tree AS (
    -- Base case: root questions
    SELECT
        id, parent_id, text, category, order_index,
        0 as depth,
        CAST(id AS TEXT) as path
    FROM questions
    WHERE parent_id IS NULL

    UNION ALL

    -- Recursive case: child questions
    SELECT
        q.id, q.parent_id, q.text, q.category, q.order_index,
        qt.depth + 1,
        qt.path || '/' || CAST(q.id AS TEXT)
    FROM questions q
    JOIN question_tree qt ON q.parent_id = qt.id
)
SELECT * FROM question_tree
ORDER BY path;

-- Get completion time for sessions
SELECT
    id,
    user_name,
    user_email,
    ROUND((julianday(completed_at) - julianday(started_at)) * 24 * 60, 2) as duration_minutes
FROM survey_sessions
WHERE completed_at IS NOT NULL;

-- ============================================
-- Useful Maintenance Queries
-- ============================================

-- Delete incomplete sessions older than 30 days
DELETE FROM survey_sessions
WHERE completed_at IS NULL
AND started_at < datetime('now', '-30 days');

-- Update category display order
UPDATE category_orders
SET order_index = ?, updated_at = CURRENT_TIMESTAMP
WHERE category = ?;

-- Reset database (DANGER - removes all data!)
-- DELETE FROM responses;
-- DELETE FROM survey_sessions;
-- DELETE FROM questions;
-- DELETE FROM category_orders;