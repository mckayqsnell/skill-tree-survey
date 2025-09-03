-- Skill Tree Survey Database Schema
-- Compatible with DrawSQL.app for visualization

-- Questions table with self-referencing for tree structure
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER,
    text TEXT NOT NULL,
    is_base BOOLEAN DEFAULT 0,
    category VARCHAR(100),
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES questions(id) ON DELETE CASCADE
);

-- Survey session tracking
CREATE TABLE survey_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name VARCHAR(200) NOT NULL,
    user_email VARCHAR(200) NOT NULL,
    company VARCHAR(200),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Individual responses
CREATE TABLE responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    answer BOOLEAN NOT NULL,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES survey_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);

-- Indexes for better query performance
CREATE INDEX idx_questions_parent_id ON questions(parent_id);
CREATE INDEX idx_questions_is_base ON questions(is_base);
CREATE INDEX idx_questions_category ON questions(category);
CREATE INDEX idx_questions_order ON questions(order_index);
CREATE INDEX idx_responses_session_id ON responses(session_id);
CREATE INDEX idx_responses_question_id ON responses(question_id);
CREATE INDEX idx_survey_sessions_email ON survey_sessions(user_email);
CREATE INDEX idx_survey_sessions_company ON survey_sessions(company);