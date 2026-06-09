// Get CloudFront URL with fallback
const CLOUDFRONT_URL = import.meta.env.VITE_CLOUDFRONT_URL || 'https://example.cloudfront.net';

// Helper function to create icon object with accessibility properties
const createIcon = (key: string, url: string) => ({
    url,
    alt: `${key.charAt(0).toUpperCase() + key.slice(1)} icon`,
    ariaLabel: `${key.charAt(0).toUpperCase() + key.slice(1)} icon`
});

// Helper function to create icon with custom alt text and aria-label
const createIconCustom = (_key: string, url: string, altText: string, ariaLabel: string) => ({
    url,
    alt: altText,
    ariaLabel: ariaLabel
});

export const icons = {
    // ===========================================
    // PROGRAMMING LANGUAGES
    // ===========================================
    python: createIcon('python', `${CLOUDFRONT_URL}/languages/python.svg`),
    typescript: createIcon('typescript', `${CLOUDFRONT_URL}/languages/typescript.svg`),
    java: createIcon('java', `${CLOUDFRONT_URL}/languages/java.svg`),
    go: createIcon('go', `${CLOUDFRONT_URL}/languages/go.svg`),
    rust: createIcon('rust', `${CLOUDFRONT_URL}/languages/rust.svg`),
    swift: createIcon('swift', `${CLOUDFRONT_URL}/languages/swift.svg`),
    kotlin: createIcon('kotlin', `${CLOUDFRONT_URL}/languages/kotlin.svg`),
    dart: createIcon('dart', `${CLOUDFRONT_URL}/languages/dart.svg`),
    scala: createIcon('scala', `${CLOUDFRONT_URL}/languages/scala.svg`),
    svelte: createIcon('svelte', `${CLOUDFRONT_URL}/languages/svelte.svg`),

    // ===========================================
    // FRONTEND FRAMEWORKS & LIBRARIES
    // ===========================================
    react: createIcon('react', `${CLOUDFRONT_URL}/frameworks/react.svg`),
    vue: createIcon('vue', `${CLOUDFRONT_URL}/frameworks/vue.svg`),
    angular: createIcon('angular', `${CLOUDFRONT_URL}/frameworks/angular.svg`),
    nextjs: createIcon('nextjs', `${CLOUDFRONT_URL}/nextjs.svg`),
    nuxt: createIcon('nuxt', `${CLOUDFRONT_URL}/frameworks/nuxt.svg`),
    remix: createIcon('remix', `${CLOUDFRONT_URL}/remix.svg`),
    gatsby: createIcon('gatsby', `${CLOUDFRONT_URL}/gatsby.svg`),
    astro: createIcon('astro', `${CLOUDFRONT_URL}/astrojs.svg`),
    tailwind: createIconCustom('tailwind', `${CLOUDFRONT_URL}/tailwindcss.svg`, 'Tailwind CSS icon', 'Tailwind CSS framework'),
    vite: createIcon('vite', `${CLOUDFRONT_URL}/frameworks/vite.svg`),
    antDesign: createIcon('antDesign', `${CLOUDFRONT_URL}/ant-design.svg`),
    materialUi: createIconCustom('materialUi', `${CLOUDFRONT_URL}/material-ui.svg`, 'Material-UI icon', 'Material-UI React component library'),
    sass: createIcon('sass', `${CLOUDFRONT_URL}/sass.svg`),
    less: createIcon('less', `${CLOUDFRONT_URL}/less.svg`),
    uikit: createIcon('uikit', `${CLOUDFRONT_URL}/uikit.svg`),

    // ===========================================
    // BACKEND FRAMEWORKS & RUNTIMES
    // ===========================================
    nodejs: createIconCustom('node.js', `${CLOUDFRONT_URL}/frameworks/nodejs.svg`, 'Node.js icon', 'Node.js JavaScript runtime'),
    express: createIcon('express', `${CLOUDFRONT_URL}/frameworks/express.svg`),
    nestjs: createIcon('nestjs', `${CLOUDFRONT_URL}/frameworks/nest.svg`),
    nest: createIcon('nest', `${CLOUDFRONT_URL}/frameworks/nest.svg`),
    django: createIcon('django', `${CLOUDFRONT_URL}/frameworks/django.svg`),
    fastapi: createIconCustom('fastapi', `${CLOUDFRONT_URL}/frameworks/fastapi.svg`, 'FastAPI icon', 'FastAPI Python web framework'),
    flask: createIcon('flask', `${CLOUDFRONT_URL}/frameworks/flask.svg`),
    spring: createIcon('spring', `${CLOUDFRONT_URL}/frameworks/spring.svg`),
    gin: createIcon('gin', `${CLOUDFRONT_URL}/gin.svg`),
    echo: createIcon('echo', `${CLOUDFRONT_URL}/frameworks/echo.png`),

    // ===========================================
    // MOBILE DEVELOPMENT
    // ===========================================
    reactNative: createIconCustom('reactNative', `${CLOUDFRONT_URL}/frameworks/react.svg`, 'React Native icon', 'React Native mobile framework'),
    flutter: createIcon('flutter', `${CLOUDFRONT_URL}/frameworks/flutter.svg`),
    xamarin: createIcon('xamarin', `${CLOUDFRONT_URL}/xamarin.svg`),
    android: createIcon('android', `${CLOUDFRONT_URL}/android.svg`),
    swiftui: createIcon('swiftui', `${CLOUDFRONT_URL}/swiftui.svg`),
    jetpackcompose: createIcon('jetpackcompose', `${CLOUDFRONT_URL}/jetpackcompose.svg`),

    // ===========================================
    // DATABASES
    // ===========================================
    mongodb: createIconCustom('mongodb', `${CLOUDFRONT_URL}/mongodb.svg`, 'MongoDB icon', 'MongoDB database'),
    mysql: createIcon('mysql', `${CLOUDFRONT_URL}/mysql.svg`),
    postgres: createIconCustom('postgres', `${CLOUDFRONT_URL}/postgres.svg`, 'PostgreSQL icon', 'PostgreSQL database'),
    dynamodb: createIconCustom('dynamodb', `${CLOUDFRONT_URL}/aws/dynamodb.svg`, 'DynamoDB icon', 'AWS DynamoDB NoSQL database'),
    redis: createIcon('redis', `${CLOUDFRONT_URL}/redis.svg`),
    couchbase: createIcon('couchbase', `${CLOUDFRONT_URL}/couchbase.svg`),
    memcached: createIcon('memcached', `${CLOUDFRONT_URL}/memcached.svg`),
    neo4j: createIcon('neo4j', `${CLOUDFRONT_URL}/neo4j.svg`),
    elasticsearch: createIcon('elasticsearch', `${CLOUDFRONT_URL}/elasticsearch.svg`),
    firestore: createIconCustom('firestore', `${CLOUDFRONT_URL}/firestore.svg`, 'Firestore icon', 'Google Firestore database'),
    cosmosdb: createIconCustom('cosmosdb', `${CLOUDFRONT_URL}/azure/cosmosdb.svg`, 'CosmosDB icon', 'Azure CosmosDB database'),
    azuresql: createIconCustom('azuresql', `${CLOUDFRONT_URL}/azure/azuresql.svg`, 'Azure SQL icon', 'Azure SQL Database'),
    bigquery: createIconCustom('bigquery', `${CLOUDFRONT_URL}/gcs/bigquery.svg`, 'BigQuery icon', 'Google BigQuery data warehouse'),
    snowflake: createIcon('snowflake', `${CLOUDFRONT_URL}/snowflake.svg`),
    teradata: createIcon('teradata', `${CLOUDFRONT_URL}/teradata.svg`),

    // ===========================================
    // AWS SERVICES
    // ===========================================
    aws: createIcon('aws', `${CLOUDFRONT_URL}/aws/aws.svg`),
    apiGateway: createIconCustom('apiGateway', `${CLOUDFRONT_URL}/aws/api-gateway.svg`, 'API Gateway icon', 'AWS API Gateway service'),
    s3: createIconCustom('s3', `${CLOUDFRONT_URL}/aws/s3.svg`, 'S3 icon', 'AWS S3 storage service'),
    cloudfront: createIconCustom('cloudfront', `${CLOUDFRONT_URL}/aws/cloudfront.svg`, 'CloudFront icon', 'AWS CloudFront CDN service'),
    cloudformation: createIconCustom('cloudformation', `${CLOUDFRONT_URL}/aws/cloudformation.svg`, 'CloudFormation icon', 'AWS CloudFormation infrastructure as code'),
    documentdb: createIconCustom('documentdb', `${CLOUDFRONT_URL}/aws/documentdb.svg`, 'DocumentDB icon', 'AWS DocumentDB database service'),
    lambda: createIconCustom('lambda', `${CLOUDFRONT_URL}/aws/lambda.svg`, 'Lambda icon', 'AWS Lambda serverless function'),
    rds: createIconCustom('rds', `${CLOUDFRONT_URL}/aws/rds.svg`, 'RDS icon', 'AWS RDS relational database service'),
    redshift: createIconCustom('redshift', `${CLOUDFRONT_URL}/aws/redshift.svg`, 'Redshift icon', 'AWS Redshift data warehouse'),
    sns: createIconCustom('sns', `${CLOUDFRONT_URL}/aws/sns.svg`, 'SNS icon', 'AWS SNS notification service'),
    sqs: createIconCustom('sqs', `${CLOUDFRONT_URL}/aws/sqs.svg`, 'SQS icon', 'AWS SQS message queue service'),
    efs: createIconCustom('efs', `${CLOUDFRONT_URL}/aws/efs.svg`, 'EFS icon', 'AWS EFS file system service'),
    ec2: createIconCustom('ec2', `${CLOUDFRONT_URL}/aws/ec2.svg`, 'EC2 icon', 'AWS EC2 compute service'),
    ecs: createIconCustom('ecs', `${CLOUDFRONT_URL}/aws/ecs.svg`, 'ECS icon', 'AWS ECS container service'),
    fargate: createIconCustom('fargate', `${CLOUDFRONT_URL}/aws/fargate.svg`, 'Fargate icon', 'AWS Fargate serverless containers'),
    iam: createIconCustom('iam', `${CLOUDFRONT_URL}/aws/iam.svg`, 'IAM icon', 'AWS IAM identity and access management'),
    sagemaker: createIconCustom('sagemaker', `${CLOUDFRONT_URL}/aws/sagemaker.svg`, 'SageMaker icon', 'AWS SageMaker machine learning platform'),
    secretsManager: createIconCustom('secretsManager', `${CLOUDFRONT_URL}/aws/secretsmanager.svg`, 'Secrets Manager icon', 'AWS Secrets Manager service'),
    ebs: createIconCustom('ebs', `${CLOUDFRONT_URL}/aws/ebs.svg`, 'EBS icon', 'AWS EBS block storage service'),

    // ===========================================
    // AZURE SERVICES
    // ===========================================
    azureDevops: createIconCustom('azureDevops', `${CLOUDFRONT_URL}/azure/azuredevops.svg`, 'Azure DevOps icon', 'Azure DevOps platform'),
    azureServiceBus: createIconCustom('azureServiceBus', `${CLOUDFRONT_URL}/azure/service-bus.svg`, 'Azure Service Bus icon', 'Azure Service Bus messaging'),
    appservice: createIconCustom('appservice', `${CLOUDFRONT_URL}/azure/appservice.svg`, 'App Service icon', 'Azure App Service'),

    // ===========================================
    // GOOGLE CLOUD SERVICES
    // ===========================================
    pubsub: createIconCustom('pubsub', `${CLOUDFRONT_URL}/gcs/pubsub.svg`, 'Pub/Sub icon', 'Google Cloud Pub/Sub messaging'),
    appengine: createIconCustom('appengine', `${CLOUDFRONT_URL}/gcs/appengine.svg`, 'App Engine icon', 'Google App Engine'),
    googlecloudfunctions: createIcon('googleCloudFunctions', `${CLOUDFRONT_URL}/gcs/google-cloud-functions.svg`),

    // ===========================================
    // CONTAINERIZATION & ORCHESTRATION
    // ===========================================
    docker: createIcon('docker', `${CLOUDFRONT_URL}/docker.svg`),
    kubernetes: createIcon('kubernetes', `${CLOUDFRONT_URL}/k8.svg`),
    helm: createIcon('helm', `${CLOUDFRONT_URL}/helm.svg`),
    argoCD: createIconCustom('argoCD', `${CLOUDFRONT_URL}/argocd.svg`, 'ArgoCD icon', 'ArgoCD GitOps continuous delivery'),

    // ===========================================
    // INFRASTRUCTURE AS CODE
    // ===========================================
    terraform: createIcon('terraform', `${CLOUDFRONT_URL}/terraform.svg`),
    ansible: createIcon('ansible', `${CLOUDFRONT_URL}/ansible.svg`),
    pulumi: createIcon('pulumi', `${CLOUDFRONT_URL}/pulumi.svg`),

    // ===========================================
    // MESSAGE QUEUES & STREAMING
    // ===========================================
    kafka: createIcon('kafka', `${CLOUDFRONT_URL}/kafka.svg`),
    rabbitmq: createIcon('rabbitmq', `${CLOUDFRONT_URL}/rabbitmq.svg`),

    // ===========================================
    // MONITORING & OBSERVABILITY
    // ===========================================
    prometheus: createIcon('prometheus', `${CLOUDFRONT_URL}/prometheus.svg`),
    grafana: createIcon('grafana', `${CLOUDFRONT_URL}/grafana.svg`),
    jaeger: createIcon('jaeger', `${CLOUDFRONT_URL}/jaeger.svg`),
    zipkin: createIcon('zipkin', `${CLOUDFRONT_URL}/zipkin.svg`),
    kibana: createIcon('kibana', `${CLOUDFRONT_URL}/kibana.svg`),
    logstash: createIcon('logstash', `${CLOUDFRONT_URL}/logstash.svg`),
    splunk: createIcon('splunk', `${CLOUDFRONT_URL}/splunk.svg`),

    // ===========================================
    // CI/CD & DEVOPS TOOLS
    // ===========================================
    git: createIcon('git', `${CLOUDFRONT_URL}/git.svg`),
    github: createIcon('github', `${CLOUDFRONT_URL}/github.svg`),
    gitlab: createIcon('gitlab', `${CLOUDFRONT_URL}/gitlab.svg`),
    jenkins: createIcon('jenkins', `${CLOUDFRONT_URL}/jenkins.svg`),
    circleci: createIcon('circleci', `${CLOUDFRONT_URL}/circleci.svg`),
    travisci: createIcon('travisci', `${CLOUDFRONT_URL}/travisci.svg`),

    // ===========================================
    // TESTING FRAMEWORKS
    // ===========================================
    jest: createIcon('jest', `${CLOUDFRONT_URL}/jest.svg`),
    cypress: createIcon('cypress', `${CLOUDFRONT_URL}/cypress.svg`),
    playwright: createIcon('playwright', `${CLOUDFRONT_URL}/playwright.svg`),
    selenium: createIcon('selenium', `${CLOUDFRONT_URL}/selenium.svg`),
    jmeter: createIcon('jmeter', `${CLOUDFRONT_URL}/jmeter.svg`),
    k6: createIcon('k6', `${CLOUDFRONT_URL}/k6.svg`),

    // ===========================================
    // API DEVELOPMENT & DOCUMENTATION
    // ===========================================
    graphql: createIcon('graphql', `${CLOUDFRONT_URL}/graphql.svg`),
    swagger: createIcon('swagger', `${CLOUDFRONT_URL}/swagger.svg`),
    postman: createIcon('postman', `${CLOUDFRONT_URL}/postman.svg`),
    grpc: createIcon('grpc', `${CLOUDFRONT_URL}/grpc.png`),
    apigee: createIconCustom('apigee', `${CLOUDFRONT_URL}/apigee.svg`, 'Apigee icon', 'Google Apigee API management'),
    kong: createIcon('kong', `${CLOUDFRONT_URL}/kong.svg`),

    // ===========================================
    // DESIGN TOOLS
    // ===========================================
    figma: createIcon('figma', `${CLOUDFRONT_URL}/figma.svg`),
    sketch: createIcon('sketch', `${CLOUDFRONT_URL}/sketch.svg`),
    adobeXd: createIconCustom('adobeXd', `${CLOUDFRONT_URL}/adobexd.svg`, 'Adobe XD icon', 'Adobe XD design tool'),

    // ===========================================
    // WEB SERVERS & PROXIES
    // ===========================================
    nginx: createIcon('nginx', `${CLOUDFRONT_URL}/nginx.svg`),

    // ===========================================
    // BUILD TOOLS & BUNDLERS
    // ===========================================
    webpack: createIcon('webpack', `${CLOUDFRONT_URL}/webpack.svg`),
    babel: createIcon('babel', `${CLOUDFRONT_URL}/babel.svg`),

    // ===========================================
    // STATE MANAGEMENT
    // ===========================================
    redux: createIcon('redux', `${CLOUDFRONT_URL}/redux.svg`),
    mobx: createIcon('mobx', `${CLOUDFRONT_URL}/mobx.svg`),
    ngrx: createIcon('ngrx', `${CLOUDFRONT_URL}/ngrx.svg`),
    ngxs: createIcon('ngxs', `${CLOUDFRONT_URL}/ngxs.png`),
    pinia: createIcon('pinia', `${CLOUDFRONT_URL}/pinia.svg`),
    vuex: createIcon('vuex', `${CLOUDFRONT_URL}/vuex.svg`),
    zustand: createIcon('zustand', `${CLOUDFRONT_URL}/zustand.svg`),
    jotai: createIcon('jotai', `${CLOUDFRONT_URL}/jotai.png`),

    // ===========================================
    // DATA SCIENCE & MACHINE LEARNING
    // ===========================================
    numpy: createIcon('numpy', `${CLOUDFRONT_URL}/data-science/numpy.svg`),
    pandas: createIcon('pandas', `${CLOUDFRONT_URL}/data-science/pandas.svg`),
    matplotlib: createIcon('matplotlib', `${CLOUDFRONT_URL}/data-science/matplotlib.svg`),
    seaborn: createIcon('seaborn', `${CLOUDFRONT_URL}/data-science/seaborn.svg`),
    plotly: createIcon('plotly', `${CLOUDFRONT_URL}/data-science/plotly.svg`),
    scikitLearn: createIconCustom('scikitLearn', `${CLOUDFRONT_URL}/data-science/scikit-learn.svg`, 'Scikit-learn icon', 'Scikit-learn machine learning library'),
    tensorflow: createIcon('tensorflow', `${CLOUDFRONT_URL}/data-science/tensorflow.svg`),
    pytorch: createIcon('pytorch', `${CLOUDFRONT_URL}/data-science/pytorch.svg`),
    scipy: createIcon('scipy', `${CLOUDFRONT_URL}/data-science/scipy.svg`),
    xgboost: createIcon('xgboost', `${CLOUDFRONT_URL}/xgboost.svg`),
    lightGBM: createIconCustom('lightGBM', `${CLOUDFRONT_URL}/lightgbm.svg`, 'LightGBM icon', 'LightGBM gradient boosting framework'),
    mlflow: createIcon('mlflow', `${CLOUDFRONT_URL}/mlflow.svg`),
    kubeflow: createIcon('kubeflow', `${CLOUDFRONT_URL}/kubeflow.svg`),

    // ===========================================
    // BIG DATA & ANALYTICS
    // ===========================================
    hadoop: createIcon('hadoop', `${CLOUDFRONT_URL}/apachehadoop.svg`),
    spark: createIcon('spark', `${CLOUDFRONT_URL}/apachespark.svg`),
    airflow: createIcon('airflow', `${CLOUDFRONT_URL}/apacheairflow.svg`),
    flink: createIcon('flink', `${CLOUDFRONT_URL}/flink.svg`),
    deltaLake: createIconCustom('deltaLake', `${CLOUDFRONT_URL}/delta-lake.png`, 'Delta Lake icon', 'Delta Lake data lake storage'),
    iceberg: createIcon('iceberg', `${CLOUDFRONT_URL}/iceberg.svg`),
    dbt: createIcon('dbt', `${CLOUDFRONT_URL}/dbt.svg`),

    // ===========================================
    // MLOPS & DATA ENGINEERING
    // ===========================================
    feast: createIcon('feast', `${CLOUDFRONT_URL}/feast.svg`),
    tecton: createIcon('tecton', `${CLOUDFRONT_URL}/tecton.svg`),
    dagster: createIcon('dagster', `${CLOUDFRONT_URL}/dagster.svg`),
    prefect: createIcon('prefect', `${CLOUDFRONT_URL}/prefect.svg`),
    dvc: createIcon('dvc', `${CLOUDFRONT_URL}/dvc.svg`),

    // ===========================================
    // SECURITY & SECRETS MANAGEMENT
    // ===========================================
    hashicorpVault: createIcon('hashicorpVault', `${CLOUDFRONT_URL}/hashicorp-vault.svg`),
    consul: createIcon('consul', `${CLOUDFRONT_URL}/consul.svg`),

    // ===========================================
    // CHAOS ENGINEERING & TESTING
    // ===========================================
    chaosMonkey: createIconCustom('chaosMonkey', `${CLOUDFRONT_URL}/chaosmonkey.svg`, 'Chaos Monkey icon', 'Netflix Chaos Monkey resilience testing'),

    // ===========================================
    // MISC TECHNOLOGIES
    // ===========================================
    xml: createIcon('xml', `${CLOUDFRONT_URL}/xml.svg`),
    flux: createIcon('flux', `${CLOUDFRONT_URL}/flux.png`),
    flyway: createIcon('flyway', `${CLOUDFRONT_URL}/flyway.svg`),
    jax: createIcon('jax', `${CLOUDFRONT_URL}/jax.svg`),
    langchain: createIcon('langchain', `${CLOUDFRONT_URL}/langchain.svg`),
    llamaindex: createIcon('llamaindex', `${CLOUDFRONT_URL}/llamaindex.svg`),
    hf: createIcon('hf', `${CLOUDFRONT_URL}/hf.svg`),
};