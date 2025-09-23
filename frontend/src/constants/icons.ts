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
    python: createIcon('python', `${import.meta.env.VITE_CLOUDFRONT_URL}/languages/python.svg`),
    typescript: createIcon('typescript', `${import.meta.env.VITE_CLOUDFRONT_URL}/languages/typescript.svg`),
    java: createIcon('java', `${import.meta.env.VITE_CLOUDFRONT_URL}/languages/java.svg`),
    go: createIcon('go', `${import.meta.env.VITE_CLOUDFRONT_URL}/languages/go.svg`),
    rust: createIcon('rust', `${import.meta.env.VITE_CLOUDFRONT_URL}/languages/rust.svg`),
    swift: createIcon('swift', `${import.meta.env.VITE_CLOUDFRONT_URL}/languages/swift.svg`),
    kotlin: createIcon('kotlin', `${import.meta.env.VITE_CLOUDFRONT_URL}/languages/kotlin.svg`),
    dart: createIcon('dart', `${import.meta.env.VITE_CLOUDFRONT_URL}/languages/dart.svg`),
    scala: createIcon('scala', `${import.meta.env.VITE_CLOUDFRONT_URL}/languages/scala.svg`),
    svelte: createIcon('svelte', `${import.meta.env.VITE_CLOUDFRONT_URL}/languages/svelte.svg`),

    // ===========================================
    // FRONTEND FRAMEWORKS & LIBRARIES
    // ===========================================
    react: createIcon('react', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/react.svg`),
    vue: createIcon('vue', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/vue.svg`),
    angular: createIcon('angular', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/angular.svg`),
    nextjs: createIcon('nextjs', `${import.meta.env.VITE_CLOUDFRONT_URL}/nextjs.svg`),
    nuxt: createIcon('nuxt', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/nuxt.svg`),
    remix: createIcon('remix', `${import.meta.env.VITE_CLOUDFRONT_URL}/remix.svg`),
    gatsby: createIcon('gatsby', `${import.meta.env.VITE_CLOUDFRONT_URL}/gatsby.svg`),
    astro: createIcon('astro', `${import.meta.env.VITE_CLOUDFRONT_URL}/astrojs.svg`),
    tailwind: createIconCustom('tailwind', `${import.meta.env.VITE_CLOUDFRONT_URL}/tailwindcss.svg`, 'Tailwind CSS icon', 'Tailwind CSS framework'),
    vite: createIcon('vite', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/vite.svg`),
    antDesign: createIcon('antDesign', `${import.meta.env.VITE_CLOUDFRONT_URL}/ant-design.svg`),
    materialUi: createIconCustom('materialUi', `${import.meta.env.VITE_CLOUDFRONT_URL}/material-ui.svg`, 'Material-UI icon', 'Material-UI React component library'),
    sass: createIcon('sass', `${import.meta.env.VITE_CLOUDFRONT_URL}/sass.svg`),
    less: createIcon('less', `${import.meta.env.VITE_CLOUDFRONT_URL}/less.svg`),
    uikit: createIcon('uikit', `${import.meta.env.VITE_CLOUDFRONT_URL}/uikit.svg`),

    // ===========================================
    // BACKEND FRAMEWORKS & RUNTIMES
    // ===========================================
    nodejs: createIconCustom('node.js', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/nodejs.svg`, 'Node.js icon', 'Node.js JavaScript runtime'),
    express: createIcon('express', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/express.svg`),
    nestjs: createIcon('nestjs', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/nest.svg`),
    nest: createIcon('nest', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/nest.svg`),
    django: createIcon('django', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/django.svg`),
    fastapi: createIconCustom('fastapi', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/fastapi.svg`, 'FastAPI icon', 'FastAPI Python web framework'),
    flask: createIcon('flask', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/flask.svg`),
    spring: createIcon('spring', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/spring.svg`),
    gin: createIcon('gin', `${import.meta.env.VITE_CLOUDFRONT_URL}/gin.svg`),
    echo: createIcon('echo', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/echo.png`),

    // ===========================================
    // MOBILE DEVELOPMENT
    // ===========================================
    reactNative: createIconCustom('reactNative', `${import.meta.env.VITE_CLOUDFRONT_URL}/react.svg`, 'React Native icon', 'React Native mobile framework'),
    flutter: createIcon('flutter', `${import.meta.env.VITE_CLOUDFRONT_URL}/frameworks/flutter.svg`),
    xamarin: createIcon('xamarin', `${import.meta.env.VITE_CLOUDFRONT_URL}/xamarin.svg`),
    android: createIcon('android', `${import.meta.env.VITE_CLOUDFRONT_URL}/android.svg`),
    swiftui: createIcon('swiftui', `${import.meta.env.VITE_CLOUDFRONT_URL}/swiftui.svg`),
    jetpackcompose: createIcon('jetpackcompose', `${import.meta.env.VITE_CLOUDFRONT_URL}/jetpackcompose.svg`),

    // ===========================================
    // DATABASES
    // ===========================================
    mongodb: createIconCustom('mongodb', `${import.meta.env.VITE_CLOUDFRONT_URL}/mongodb.svg`, 'MongoDB icon', 'MongoDB database'),
    mysql: createIcon('mysql', `${import.meta.env.VITE_CLOUDFRONT_URL}/mysql.svg`),
    postgres: createIconCustom('postgres', `${import.meta.env.VITE_CLOUDFRONT_URL}/postgres.svg`, 'PostgreSQL icon', 'PostgreSQL database'),
    dynamodb: createIconCustom('dynamodb', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/dynamodb.svg`, 'DynamoDB icon', 'AWS DynamoDB NoSQL database'),
    redis: createIcon('redis', `${import.meta.env.VITE_CLOUDFRONT_URL}/redis.svg`),
    couchbase: createIcon('couchbase', `${import.meta.env.VITE_CLOUDFRONT_URL}/couchbase.svg`),
    memcached: createIcon('memcached', `${import.meta.env.VITE_CLOUDFRONT_URL}/memcached.svg`),
    neo4j: createIcon('neo4j', `${import.meta.env.VITE_CLOUDFRONT_URL}/neo4j.svg`),
    elasticsearch: createIcon('elasticsearch', `${import.meta.env.VITE_CLOUDFRONT_URL}/elasticsearch.svg`),
    firestore: createIconCustom('firestore', `${import.meta.env.VITE_CLOUDFRONT_URL}/firestore.svg`, 'Firestore icon', 'Google Firestore database'),
    cosmosdb: createIconCustom('cosmosdb', `${import.meta.env.VITE_CLOUDFRONT_URL}/azure/cosmosdb.svg`, 'CosmosDB icon', 'Azure CosmosDB database'),
    azuresql: createIconCustom('azuresql', `${import.meta.env.VITE_CLOUDFRONT_URL}/azure/azuresql.svg`, 'Azure SQL icon', 'Azure SQL Database'),
    bigquery: createIconCustom('bigquery', `${import.meta.env.VITE_CLOUDFRONT_URL}/gcs/bigquery.svg`, 'BigQuery icon', 'Google BigQuery data warehouse'),
    snowflake: createIcon('snowflake', `${import.meta.env.VITE_CLOUDFRONT_URL}/snowflake.svg`),
    teradata: createIcon('teradata', `${import.meta.env.VITE_CLOUDFRONT_URL}/teradata.svg`),

    // ===========================================
    // AWS SERVICES
    // ===========================================
    aws: createIcon('aws', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/aws.svg`),
    apiGateway: createIconCustom('apiGateway', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/api-gateway.svg`, 'API Gateway icon', 'AWS API Gateway service'),
    s3: createIconCustom('s3', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/s3.svg`, 'S3 icon', 'AWS S3 storage service'),
    cloudfront: createIconCustom('cloudfront', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/cloudfront.svg`, 'CloudFront icon', 'AWS CloudFront CDN service'),
    cloudformation: createIconCustom('cloudformation', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/cloudformation.svg`, 'CloudFormation icon', 'AWS CloudFormation infrastructure as code'),
    documentdb: createIconCustom('documentdb', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/documentdb.svg`, 'DocumentDB icon', 'AWS DocumentDB database service'),
    lambda: createIconCustom('lambda', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/lambda.svg`, 'Lambda icon', 'AWS Lambda serverless function'),
    rds: createIconCustom('rds', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/rds.svg`, 'RDS icon', 'AWS RDS relational database service'),
    redshift: createIconCustom('redshift', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/redshift.svg`, 'Redshift icon', 'AWS Redshift data warehouse'),
    sns: createIconCustom('sns', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/sns.svg`, 'SNS icon', 'AWS SNS notification service'),
    sqs: createIconCustom('sqs', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/sqs.svg`, 'SQS icon', 'AWS SQS message queue service'),
    efs: createIconCustom('efs', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/efs.svg`, 'EFS icon', 'AWS EFS file system service'),
    ec2: createIconCustom('ec2', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/ec2.svg`, 'EC2 icon', 'AWS EC2 compute service'),
    ecs: createIconCustom('ecs', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/ecs.svg`, 'ECS icon', 'AWS ECS container service'),
    fargate: createIconCustom('fargate', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/fargate.svg`, 'Fargate icon', 'AWS Fargate serverless containers'),
    iam: createIconCustom('iam', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/iam.svg`, 'IAM icon', 'AWS IAM identity and access management'),
    sagemaker: createIconCustom('sagemaker', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/sagemaker.svg`, 'SageMaker icon', 'AWS SageMaker machine learning platform'),
    secretsManager: createIconCustom('secretsManager', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/secretsmanager.svg`, 'Secrets Manager icon', 'AWS Secrets Manager service'),
    ebs: createIconCustom('ebs', `${import.meta.env.VITE_CLOUDFRONT_URL}/aws/ebs.svg`, 'EBS icon', 'AWS EBS block storage service'),

    // ===========================================
    // AZURE SERVICES
    // ===========================================
    azureDevops: createIconCustom('azureDevops', `${import.meta.env.VITE_CLOUDFRONT_URL}/azure/azuredevops.svg`, 'Azure DevOps icon', 'Azure DevOps platform'),
    azureServiceBus: createIconCustom('azureServiceBus', `${import.meta.env.VITE_CLOUDFRONT_URL}/azure/service-bus.svg`, 'Azure Service Bus icon', 'Azure Service Bus messaging'),
    appservice: createIconCustom('appservice', `${import.meta.env.VITE_CLOUDFRONT_URL}/azure/appservice.svg`, 'App Service icon', 'Azure App Service'),

    // ===========================================
    // GOOGLE CLOUD SERVICES
    // ===========================================
    pubsub: createIconCustom('pubsub', `${import.meta.env.VITE_CLOUDFRONT_URL}/gcs/pubsub.svg`, 'Pub/Sub icon', 'Google Cloud Pub/Sub messaging'),
    appengine: createIconCustom('appengine', `${import.meta.env.VITE_CLOUDFRONT_URL}/gcs/appengine.svg`, 'App Engine icon', 'Google App Engine'),
    googlecloudfunctions: createIcon('googleCloudFunctions', `${import.meta.env.VITE_CLOUDFRONT_URL}/gcs/google-cloud-functions.svg`),

    // ===========================================
    // CONTAINERIZATION & ORCHESTRATION
    // ===========================================
    docker: createIcon('docker', `${import.meta.env.VITE_CLOUDFRONT_URL}/docker.svg`),
    kubernetes: createIcon('kubernetes', `${import.meta.env.VITE_CLOUDFRONT_URL}/k8.svg`),
    helm: createIcon('helm', `${import.meta.env.VITE_CLOUDFRONT_URL}/helm.svg`),
    argoCD: createIconCustom('argoCD', `${import.meta.env.VITE_CLOUDFRONT_URL}/argocd.svg`, 'ArgoCD icon', 'ArgoCD GitOps continuous delivery'),

    // ===========================================
    // INFRASTRUCTURE AS CODE
    // ===========================================
    terraform: createIcon('terraform', `${import.meta.env.VITE_CLOUDFRONT_URL}/terraform.svg`),
    ansible: createIcon('ansible', `${import.meta.env.VITE_CLOUDFRONT_URL}/ansible.svg`),
    pulumi: createIcon('pulumi', `${import.meta.env.VITE_CLOUDFRONT_URL}/pulumi.svg`),

    // ===========================================
    // MESSAGE QUEUES & STREAMING
    // ===========================================
    kafka: createIcon('kafka', `${import.meta.env.VITE_CLOUDFRONT_URL}/kafka.svg`),
    rabbitmq: createIcon('rabbitmq', `${import.meta.env.VITE_CLOUDFRONT_URL}/rabbitmq.svg`),

    // ===========================================
    // MONITORING & OBSERVABILITY
    // ===========================================
    prometheus: createIcon('prometheus', `${import.meta.env.VITE_CLOUDFRONT_URL}/prometheus.svg`),
    grafana: createIcon('grafana', `${import.meta.env.VITE_CLOUDFRONT_URL}/grafana.svg`),
    jaeger: createIcon('jaeger', `${import.meta.env.VITE_CLOUDFRONT_URL}/jaeger.svg`),
    zipkin: createIcon('zipkin', `${import.meta.env.VITE_CLOUDFRONT_URL}/zipkin.svg`),
    kibana: createIcon('kibana', `${import.meta.env.VITE_CLOUDFRONT_URL}/kibana.svg`),
    logstash: createIcon('logstash', `${import.meta.env.VITE_CLOUDFRONT_URL}/logstash.svg`),
    splunk: createIcon('splunk', `${import.meta.env.VITE_CLOUDFRONT_URL}/splunk.svg`),

    // ===========================================
    // CI/CD & DEVOPS TOOLS
    // ===========================================
    git: createIcon('git', `${import.meta.env.VITE_CLOUDFRONT_URL}/git.svg`),
    github: createIcon('github', `${import.meta.env.VITE_CLOUDFRONT_URL}/github.svg`),
    gitlab: createIcon('gitlab', `${import.meta.env.VITE_CLOUDFRONT_URL}/gitlab.svg`),
    jenkins: createIcon('jenkins', `${import.meta.env.VITE_CLOUDFRONT_URL}/jenkins.svg`),
    circleci: createIcon('circleci', `${import.meta.env.VITE_CLOUDFRONT_URL}/circleci.svg`),
    travisci: createIcon('travisci', `${import.meta.env.VITE_CLOUDFRONT_URL}/travisci.svg`),

    // ===========================================
    // TESTING FRAMEWORKS
    // ===========================================
    jest: createIcon('jest', `${import.meta.env.VITE_CLOUDFRONT_URL}/jest.svg`),
    cypress: createIcon('cypress', `${import.meta.env.VITE_CLOUDFRONT_URL}/cypress.svg`),
    playwright: createIcon('playwright', `${import.meta.env.VITE_CLOUDFRONT_URL}/playwright.svg`),
    selenium: createIcon('selenium', `${import.meta.env.VITE_CLOUDFRONT_URL}/selenium.svg`),
    jmeter: createIcon('jmeter', `${import.meta.env.VITE_CLOUDFRONT_URL}/jmeter.svg`),
    k6: createIcon('k6', `${import.meta.env.VITE_CLOUDFRONT_URL}/k6.svg`),

    // ===========================================
    // API DEVELOPMENT & DOCUMENTATION
    // ===========================================
    graphql: createIcon('graphql', `${import.meta.env.VITE_CLOUDFRONT_URL}/graphql.svg`),
    swagger: createIcon('swagger', `${import.meta.env.VITE_CLOUDFRONT_URL}/swagger.svg`),
    postman: createIcon('postman', `${import.meta.env.VITE_CLOUDFRONT_URL}/postman.svg`),
    grpc: createIcon('grpc', `${import.meta.env.VITE_CLOUDFRONT_URL}/grpc.png`),
    apigee: createIconCustom('apigee', `${import.meta.env.VITE_CLOUDFRONT_URL}/apigee.svg`, 'Apigee icon', 'Google Apigee API management'),
    kong: createIcon('kong', `${import.meta.env.VITE_CLOUDFRONT_URL}/kong.svg`),

    // ===========================================
    // DESIGN TOOLS
    // ===========================================
    figma: createIcon('figma', `${import.meta.env.VITE_CLOUDFRONT_URL}/figma.svg`),
    sketch: createIcon('sketch', `${import.meta.env.VITE_CLOUDFRONT_URL}/sketch.svg`),
    adobeXd: createIconCustom('adobeXd', `${import.meta.env.VITE_CLOUDFRONT_URL}/adobexd.svg`, 'Adobe XD icon', 'Adobe XD design tool'),

    // ===========================================
    // WEB SERVERS & PROXIES
    // ===========================================
    nginx: createIcon('nginx', `${import.meta.env.VITE_CLOUDFRONT_URL}/nginx.svg`),

    // ===========================================
    // BUILD TOOLS & BUNDLERS
    // ===========================================
    webpack: createIcon('webpack', `${import.meta.env.VITE_CLOUDFRONT_URL}/webpack.svg`),
    babel: createIcon('babel', `${import.meta.env.VITE_CLOUDFRONT_URL}/babel.svg`),

    // ===========================================
    // STATE MANAGEMENT
    // ===========================================
    redux: createIcon('redux', `${import.meta.env.VITE_CLOUDFRONT_URL}/redux.svg`),
    mobx: createIcon('mobx', `${import.meta.env.VITE_CLOUDFRONT_URL}/mobx.svg`),
    ngrx: createIcon('ngrx', `${import.meta.env.VITE_CLOUDFRONT_URL}/ngrx.svg`),
    ngxs: createIcon('ngxs', `${import.meta.env.VITE_CLOUDFRONT_URL}/ngxs.png`),
    pinia: createIcon('pinia', `${import.meta.env.VITE_CLOUDFRONT_URL}/pinia.svg`),
    vuex: createIcon('vuex', `${import.meta.env.VITE_CLOUDFRONT_URL}/vuex.svg`),
    zustand: createIcon('zustand', `${import.meta.env.VITE_CLOUDFRONT_URL}/zustand.svg`),
    jotai: createIcon('jotai', `${import.meta.env.VITE_CLOUDFRONT_URL}/jotai.png`),

    // ===========================================
    // DATA SCIENCE & MACHINE LEARNING
    // ===========================================
    numpy: createIcon('numpy', `${import.meta.env.VITE_CLOUDFRONT_URL}/data-science/numpy.svg`),
    pandas: createIcon('pandas', `${import.meta.env.VITE_CLOUDFRONT_URL}/data-science/pandas.svg`),
    matplotlib: createIcon('matplotlib', `${import.meta.env.VITE_CLOUDFRONT_URL}/data-science/matplotlib.svg`),
    seaborn: createIcon('seaborn', `${import.meta.env.VITE_CLOUDFRONT_URL}/data-science/seaborn.svg`),
    plotly: createIcon('plotly', `${import.meta.env.VITE_CLOUDFRONT_URL}/data-science/plotly.svg`),
    scikitLearn: createIconCustom('scikitLearn', `${import.meta.env.VITE_CLOUDFRONT_URL}/data-science/scikit-learn.svg`, 'Scikit-learn icon', 'Scikit-learn machine learning library'),
    tensorflow: createIcon('tensorflow', `${import.meta.env.VITE_CLOUDFRONT_URL}/data-science/tensorflow.svg`),
    pytorch: createIcon('pytorch', `${import.meta.env.VITE_CLOUDFRONT_URL}/data-science/pytorch.svg`),
    scipy: createIcon('scipy', `${import.meta.env.VITE_CLOUDFRONT_URL}/data-science/scipy.svg`),
    xgboost: createIcon('xgboost', `${import.meta.env.VITE_CLOUDFRONT_URL}/xgboost.svg`),
    lightGBM: createIconCustom('lightGBM', `${import.meta.env.VITE_CLOUDFRONT_URL}/lightgbm.svg`, 'LightGBM icon', 'LightGBM gradient boosting framework'),
    mlflow: createIcon('mlflow', `${import.meta.env.VITE_CLOUDFRONT_URL}/mlflow.svg`),
    kubeflow: createIcon('kubeflow', `${import.meta.env.VITE_CLOUDFRONT_URL}/kubeflow.svg`),

    // ===========================================
    // BIG DATA & ANALYTICS
    // ===========================================
    hadoop: createIcon('hadoop', `${import.meta.env.VITE_CLOUDFRONT_URL}/apachehadoop.svg`),
    spark: createIcon('spark', `${import.meta.env.VITE_CLOUDFRONT_URL}/apachespark.svg`),
    airflow: createIcon('airflow', `${import.meta.env.VITE_CLOUDFRONT_URL}/apacheairflow.svg`),
    flink: createIcon('flink', `${import.meta.env.VITE_CLOUDFRONT_URL}/flink.svg`),
    deltaLake: createIconCustom('deltaLake', `${import.meta.env.VITE_CLOUDFRONT_URL}/delta-lake.png`, 'Delta Lake icon', 'Delta Lake data lake storage'),
    iceberg: createIcon('iceberg', `${import.meta.env.VITE_CLOUDFRONT_URL}/iceberg.svg`),
    dbt: createIcon('dbt', `${import.meta.env.VITE_CLOUDFRONT_URL}/dbt.svg`),

    // ===========================================
    // MLOPS & DATA ENGINEERING
    // ===========================================
    feast: createIcon('feast', `${import.meta.env.VITE_CLOUDFRONT_URL}/feast.svg`),
    tecton: createIcon('tecton', `${import.meta.env.VITE_CLOUDFRONT_URL}/tecton.svg`),
    dagster: createIcon('dagster', `${import.meta.env.VITE_CLOUDFRONT_URL}/dagster.svg`),
    prefect: createIcon('prefect', `${import.meta.env.VITE_CLOUDFRONT_URL}/prefect.svg`),
    dvc: createIcon('dvc', `${import.meta.env.VITE_CLOUDFRONT_URL}/dvc.svg`),

    // ===========================================
    // SECURITY & SECRETS MANAGEMENT
    // ===========================================
    hashicorpVault: createIcon('hashicorpVault', `${import.meta.env.VITE_CLOUDFRONT_URL}/hashicorp-vault.svg`),
    consul: createIcon('consul', `${import.meta.env.VITE_CLOUDFRONT_URL}/consul.svg`),

    // ===========================================
    // CHAOS ENGINEERING & TESTING
    // ===========================================
    chaosMonkey: createIconCustom('chaosMonkey', `${import.meta.env.VITE_CLOUDFRONT_URL}/chaosmonkey.svg`, 'Chaos Monkey icon', 'Netflix Chaos Monkey resilience testing'),

    // ===========================================
    // MISC TECHNOLOGIES
    // ===========================================
    xml: createIcon('xml', `${import.meta.env.VITE_CLOUDFRONT_URL}/xml.svg`),
    flux: createIcon('flux', `${import.meta.env.VITE_CLOUDFRONT_URL}/flux.png`),
    flyway: createIcon('flyway', `${import.meta.env.VITE_CLOUDFRONT_URL}/flyway.svg`),
    jax: createIcon('jax', `${import.meta.env.VITE_CLOUDFRONT_URL}/jax.svg`),
    langchain: createIcon('langchain', `${import.meta.env.VITE_CLOUDFRONT_URL}/langchain.svg`),
    llamaindex: createIcon('llamaindex', `${import.meta.env.VITE_CLOUDFRONT_URL}/llamaindex.svg`),
    hf: createIcon('hf', `${import.meta.env.VITE_CLOUDFRONT_URL}/hf.svg`),
};