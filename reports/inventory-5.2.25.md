# 全量清单与批次切分报告（v5.2.25 基线）

- 基线：micronaut-core@0b46d27afdfa（tag v5.2.25），快照 2026-11-20
- 账本：388 条目（含 guide/toc.yml、guide/toc-python.yml），missing 386 / skipped 2
- 词数总计：非代码词 99722 / 总词 100312 / 总段 5573（口径：保护后 wc -w 等价）
- 批次：32 个（双指标 非代码词 ≤3500 且 总词 ≤5500，toc 顺序贪心装箱）

## toc.yml 实测结论

- **含显示标题**：toc.yml 为嵌套 dict（键→显示标题），与 toc-python.yml （Python 文风定制版）共 30KB；两者均已入账本（可译对象为标题值，YAML 键不译）。
- 键路径 → 文件映射：`guide/<键路径>.adoc`（DFS 序即阅读顺序）；toc 覆盖 385 个文件，未入 toc 的 include 片段 1 个（按目录序追加在批次末尾）。
- 纯 include 壳文件 2 个（guide/appendix.adoc、guide/i18n.adoc）标 skipped，不进批次。

## 批次切分表

| 批次 | 文件数 | 非代码词 | 总词 |
|---|---:|---:|---:|
| B01 | 19 | 3347 | 3355 |
| B02 | 12 | 3049 | 3082 |
| B03 | 10 | 3443 | 3454 |
| B04 | 19 | 2591 | 2604 |
| B05 | 2 | 2138 | 2128 |
| B06 | 11 | 3454 | 3489 |
| B07 | 4 | 2507 | 2554 |
| B08 | 4 | 3397 | 3442 |
| B09 | 8 | 2915 | 2915 |
| B10 | 5 | 3086 | 3092 |
| B11 | 7 | 3350 | 3352 |
| B12 | 25 | 3454 | 3460 |
| B13 | 17 | 3167 | 3185 |
| B14 | 13 | 3482 | 3476 |
| B15 | 13 | 3452 | 3485 |
| B16 | 24 | 3223 | 3291 |
| B17 | 15 | 3004 | 3008 |
| B18 | 8 | 3379 | 3379 |
| B19 | 14 | 3455 | 3491 |
| B20 | 21 | 3456 | 3512 |
| B21 | 35 | 2983 | 3078 |
| B22 | 5 | 3062 | 3057 |
| B23 | 6 | 3378 | 3353 |
| B24 | 5 | 3257 | 3199 |
| B25 | 7 | 3096 | 3070 |
| B26 | 14 | 3416 | 3439 |
| B27 | 17 | 3478 | 3538 |
| B28 | 21 | 2955 | 3023 |
| B29 | 14 | 3226 | 3257 |
| B30 | 4 | 3387 | 3401 |
| B31 | 3 | 955 | 960 |
| B32 | 2 | 3180 | 3183 |

## 逐批次文件清单

### B01（非代码词 3347 / 总词 3355）

`guide/introduction.adoc`、`guide/introduction/whatsNew.adoc`、`guide/introduction/upgrading.adoc`、`guide/quickStart.adoc`、`guide/quickStart/buildCLI.adoc`、`guide/quickStart/creatingServer.adoc`、`guide/quickStart/ideSetup.adoc`、`guide/quickStart/ideSetup/ideaSetup.adoc`、`guide/quickStart/ideSetup/vsCodeSetup.adoc`、`guide/quickStart/ideSetup/eclipseSetup.adoc`、`guide/quickStart/ideSetup/netbeansSetup.adoc`、`guide/quickStart/creatingClient.adoc`、`guide/quickStart/deployingApp.adoc`、`guide/ioc.adoc`、`guide/ioc/beans.adoc`、`guide/ioc/how.adoc`、`guide/ioc/iocDebugging.adoc`、`guide/ioc/beanContext.adoc`、`guide/ioc/injection.adoc`

### B02（非代码词 3049 / 总词 3082）

`guide/ioc/injection/constructorInjection.adoc`、`guide/ioc/injection/fieldInjection.adoc`、`guide/ioc/injection/methodInjection.adoc`、`guide/ioc/injection/nullableInjection.adoc`、`guide/ioc/types.adoc`、`guide/ioc/qualifiers.adoc`、`guide/ioc/typed.adoc`、`guide/ioc/scopes.adoc`、`guide/ioc/scopes/builtInScopes.adoc`、`guide/ioc/scopes/builtInScopes/eagerInit.adoc`、`guide/ioc/scopes/refreshable.adoc`、`guide/ioc/scopes/metaScopes.adoc`

### B03（非代码词 3443 / 总词 3454）

`guide/ioc/factories.adoc`、`guide/ioc/conditionalBeans.adoc`、`guide/ioc/replaces.adoc`、`guide/ioc/beanConfigurations.adoc`、`guide/ioc/lifecycle.adoc`、`guide/ioc/gracefulShutdown.adoc`、`guide/ioc/contextEvents.adoc`、`guide/ioc/events.adoc`、`guide/ioc/introspection.adoc`、`guide/ioc/introspection/makingABeanAvailableForIntrospection.adoc`

### B04（非代码词 2591 / 总词 2604）

`guide/ioc/introspection/atIntrospected.adoc`、`guide/ioc/introspection/introspectedAccessorsStyle.adoc`、`guide/ioc/introspection/accessKind.adoc`、`guide/ioc/introspection/introspectedProperty.adoc`、`guide/ioc/introspection/propertyMembers.adoc`、`guide/ioc/introspection/atCreator.adoc`、`guide/ioc/introspection/staticAtCreator.adoc`、`guide/ioc/introspection/introspectionConstructors.adoc`、`guide/ioc/introspection/introspectionBuilders.adoc`、`guide/ioc/introspection/introspectionEnums.adoc`、`guide/ioc/introspection/introspectionTypeArguments.adoc`、`guide/ioc/introspection/introspectedAnnotationOnAConfigurationClass.adoc`、`guide/ioc/introspection/introspectExistingAnnotations.adoc`、`guide/ioc/introspection/beanWrapperApi.adoc`、`guide/ioc/introspection/kotlinAndBeanIntrospection.adoc`、`guide/ioc/beanMappers.adoc`、`guide/ioc/beanMappers/beanMappersMerging.adoc`、`guide/ioc/beanMappers/beanMappersMerging/beanMappersMergingStrategy.adoc`、`guide/ioc/beanValidation.adoc`

### B05（非代码词 2138 / 总词 2128）

`guide/ioc/annotationMetadata.adoc`、`guide/ioc/beanImport.adoc`

### B06（非代码词 3454 / 总词 3489）

`guide/ioc/reflection.adoc`、`guide/ioc/classImport.adoc`、`guide/ioc/mixin.adoc`、`guide/ioc/nullabilityAnnotations.adoc`、`guide/ioc/nullabilityAnnotations/jspecify.adoc`、`guide/ioc/springBeans.adoc`、`guide/ioc/android.adoc`、`guide/config.adoc`、`guide/config/environments.adoc`、`guide/config/environments/environmentPriority.adoc`、`guide/config/environments/disablingEnvironmentDetection.adoc`

### B07（非代码词 2507 / 总词 2554）

`guide/config/environments/defaultEnvironment.adoc`、`guide/config/banner.adoc`、`guide/config/propertySource.adoc`、`guide/config/valueAnnotation.adoc`

### B08（非代码词 3397 / 总词 3442）

`guide/config/evaluatedExpressions.adoc`、`guide/config/configurationProperties.adoc`、`guide/config/customTypeConverter.adoc`、`guide/config/eachProperty.adoc`

### B09（非代码词 2915 / 总词 2915）

`guide/config/eachBean.adoc`、`guide/config/immutableConfig.adoc`、`guide/config/bootstrap.adoc`、`guide/config/jmx.adoc`、`guide/aop.adoc`、`guide/aop/aroundAdvice.adoc`、`guide/aop/introductionAdvice.adoc`、`guide/aop/adapterAdvice.adoc`

### B10（非代码词 3086 / 总词 3092）

`guide/aop/lifecycleAdvice.adoc`、`guide/aop/interceptorLifecycle.adoc`、`guide/aop/validation.adoc`、`guide/aop/caching.adoc`、`guide/aop/retry.adoc`

### B11（非代码词 3350 / 总词 3352）

`guide/aop/scheduling.adoc`、`guide/aop/springAop.adoc`、`guide/httpServer.adoc`、`guide/httpServer/runningServer.adoc`、`guide/httpServer/runningSpecificPort.adoc`、`guide/httpServer/routing.adoc`、`guide/httpServer/binding.adoc`

### B12（非代码词 3454 / 总词 3460）

`guide/httpServer/customArgumentBinding.adoc`、`guide/httpServer/hostResolution.adoc`、`guide/httpServer/localeResolution.adoc`、`guide/httpServer/clientIpAddress.adoc`、`guide/httpServer/requestResponse.adoc`、`guide/httpServer/statusAnnotation.adoc`、`guide/httpServer/producesAnnotation.adoc`、`guide/httpServer/consumesAnnotation.adoc`、`guide/httpServer/reactiveServer.adoc`、`guide/httpServer/reactiveServer/bodyAnnotation.adoc`、`guide/httpServer/reactiveServer/reactiveResponses.adoc`、`guide/httpServer/jsonBinding.adoc`、`guide/httpServer/jsonBinding/serializeUsingMicronautSerialization.adoc`、`guide/httpServer/jsonBinding/serializationUsingJacksonDatabind.adoc`、`guide/httpServer/jsonBinding/jsonMapper.adoc`、`guide/httpServer/jsonBinding/bindingUsingReactiveFrameworks.adoc`、`guide/httpServer/jsonBinding/bindingUsingCompletableFuture.adoc`、`guide/httpServer/jsonBinding/bindingUsingPOJOs.adoc`、`guide/httpServer/jsonBinding/jacksonConfiguration.adoc`、`guide/httpServer/jsonBinding/jacksonConfiguration/jacksonConfigurationFeatures.adoc`、`guide/httpServer/jsonBinding/jacksonConfiguration/jacksonConfigurationFurtherCustomisingJsonFactory.adoc`、`guide/httpServer/jsonBinding/jacksonConfiguration/jacksonConfigurationSupportForJsonView.adoc`、`guide/httpServer/jsonBinding/jacksonConfiguration/jacksonConfigurationBeans.adoc`、`guide/httpServer/jsonBinding/jacksonConfiguration/jacksonConfigurationServiceLoader.adoc`、`guide/httpServer/jsonBinding/jacksonConfiguration/jacksonConfigurationNumberPrecision.adoc`

### B13（非代码词 3167 / 总词 3185）

`guide/httpServer/plainTextResponses.adoc`、`guide/httpServer/datavalidation.adoc`、`guide/httpServer/datavalidation/validationGroups.adoc`、`guide/httpServer/staticResources.adoc`、`guide/httpServer/errorHandling.adoc`、`guide/httpServer/errorHandling/statusHandlers.adoc`、`guide/httpServer/errorHandling/localErrorHandling.adoc`、`guide/httpServer/errorHandling/globalErrorHandling.adoc`、`guide/httpServer/errorHandling/exceptionHandler.adoc`、`guide/httpServer/errorHandling/exceptionHandler/builtInExceptionHandlers.adoc`、`guide/httpServer/errorHandling/exceptionHandler/customExceptionHandler.adoc`、`guide/httpServer/errorHandling/errorFormatting.adoc`、`guide/httpServer/apiVersioning.adoc`、`guide/httpServer/formData.adoc`、`guide/httpServer/form.adoc`、`guide/httpServer/form/formBinding.adoc`、`guide/httpServer/form/formCapable.adoc`

### B14（非代码词 3482 / 总词 3476）

`guide/httpServer/serverIO.adoc`、`guide/httpServer/uploads.adoc`、`guide/httpServer/transfers.adoc`、`guide/httpServer/filters.adoc`、`guide/httpServer/filters/filterPatterns.adoc`、`guide/httpServer/filters/filtermethods.adoc`、`guide/httpServer/filters/filtermethods/filtermethodsexample.adoc`、`guide/httpServer/filters/filtermethods/filtermethodproceed.adoc`、`guide/httpServer/filters/filtermethods/errorStates.adoc`、`guide/httpServer/filters/filtermethods/continuations.adoc`、`guide/httpServer/filters/filtermethods/order.adoc`、`guide/httpServer/filters/httpServerFilter.adoc`、`guide/httpServer/filters/httpServerFilter/httpServerFilterExample.adoc`

### B15（非代码词 3452 / 总词 3485）

`guide/httpServer/filters/httpServerFilter/httpServerFilterErrorStates.adoc`、`guide/httpServer/filters/responseHeaderPopulator.adoc`、`guide/httpServer/byteBody.adoc`、`guide/httpServer/byteBody/byteBodyPrimary.adoc`、`guide/httpServer/byteBody/byteBodySplitting.adoc`、`guide/httpServer/byteBody/byteBodyExample.adoc`、`guide/httpServer/sessions.adoc`、`guide/httpServer/sse.adoc`、`guide/httpServer/websocket.adoc`、`guide/httpServer/websocket/websocketServer.adoc`、`guide/httpServer/websocket/websocketClient.adoc`、`guide/httpServer/http2Server.adoc`、`guide/httpServer/http3Server.adoc`

### B16（非代码词 3223 / 总词 3291）

`guide/httpServer/serverEvents.adoc`、`guide/httpServer/serverConfiguration.adoc`、`guide/httpServer/serverConfiguration/threadPools.adoc`、`guide/httpServer/serverConfiguration/threadPools/blockingOperations.adoc`、`guide/httpServer/serverConfiguration/threadPools/virtualThreads.adoc`、`guide/httpServer/serverConfiguration/threadPools/atBlocking.adoc`、`guide/httpServer/serverConfiguration/nettyClientPipeline.adoc`、`guide/httpServer/serverConfiguration/nettyServerPipeline.adoc`、`guide/httpServer/serverConfiguration/listener.adoc`、`guide/httpServer/serverConfiguration/corsCrossOriginEmbedderPolicy.adoc`、`guide/httpServer/serverConfiguration/corsCrossOriginResourcePolicy.adoc`、`guide/httpServer/serverConfiguration/cors.adoc`、`guide/httpServer/serverConfiguration/cors/annotationBasedCors.adoc`、`guide/httpServer/serverConfiguration/cors/corsConfiguration.adoc`、`guide/httpServer/serverConfiguration/cors/corsAllowedOrigins.adoc`、`guide/httpServer/serverConfiguration/cors/corsAllowedMethods.adoc`、`guide/httpServer/serverConfiguration/cors/corsAllowedHeaders.adoc`、`guide/httpServer/serverConfiguration/cors/corsExposedHeaders.adoc`、`guide/httpServer/serverConfiguration/cors/corsAllowCredentials.adoc`、`guide/httpServer/serverConfiguration/cors/corsAllowPrivateNetwork.adoc`、`guide/httpServer/serverConfiguration/cors/corsMaxAge.adoc`、`guide/httpServer/serverConfiguration/cors/corsMultipleHeaderValues.adoc`、`guide/httpServer/serverConfiguration/https.adoc`、`guide/httpServer/serverConfiguration/dualProtocol.adoc`

### B17（非代码词 3004 / 总词 3008）

`guide/httpServer/serverConfiguration/accessLogger.adoc`、`guide/httpServer/serverConfiguration/secondaryServers.adoc`、`guide/httpServer/views.adoc`、`guide/httpServer/openapi.adoc`、`guide/httpServer/graphql.adoc`、`guide/httpClient.adoc`、`guide/httpClient/httpClientImplementations.adoc`、`guide/httpClient/httpClientImplementations/nettyHttpClient.adoc`、`guide/httpClient/httpClientImplementations/jdkHttpClient.adoc`、`guide/httpClient/lowLevelOrHighLevel.adoc`、`guide/httpClient/lowLevelHttpClient.adoc`、`guide/httpClient/lowLevelHttpClient/clientBasics.adoc`、`guide/httpClient/lowLevelHttpClient/clientPostRequests.adoc`、`guide/httpClient/lowLevelHttpClient/clientUploads.adoc`、`guide/httpClient/lowLevelHttpClient/clientStreaming.adoc`

### B18（非代码词 3379 / 总词 3379）

`guide/httpClient/lowLevelHttpClient/clientConfiguration.adoc`、`guide/httpClient/lowLevelHttpClient/lowLevelClientError.adoc`、`guide/httpClient/lowLevelHttpClient/bindErrors.adoc`、`guide/httpClient/proxyClient.adoc`、`guide/httpClient/clientAnnotation.adoc`、`guide/httpClient/clientAnnotation/clientParameters.adoc`、`guide/httpClient/clientAnnotation/clientAnnotationStreaming.adoc`、`guide/httpClient/clientAnnotation/clientError.adoc`

### B19（非代码词 3455 / 总词 3491）

`guide/httpClient/clientAnnotation/clientHeaders.adoc`、`guide/httpClient/clientAnnotation/clientJackson.adoc`、`guide/httpClient/clientAnnotation/clientRetry.adoc`、`guide/httpClient/clientAnnotation/clientFallback.adoc`、`guide/httpClient/clientFilter.adoc`、`guide/httpClient/clientHttp2.adoc`、`guide/httpClient/clientHttp3.adoc`、`guide/httpClient/clientSample.adoc`、`guide/httpClient/nettyPooling.adoc`、`guide/certificates.adoc`、`guide/contextPropagation.adoc`、`guide/contextPropagation/reactorContextPropagation.adoc`、`guide/contextPropagation/httpFilterContextPropagation.adoc`、`guide/cloud.adoc`

### B20（非代码词 3456 / 总词 3512）

`guide/cloud/cloudConfiguration.adoc`、`guide/cloud/cloudConfiguration/distributedConfiguration.adoc`、`guide/cloud/cloudConfiguration/distributedConfigurationConsul.adoc`、`guide/cloud/cloudConfiguration/distributedConfigurationVault.adoc`、`guide/cloud/cloudConfiguration/distributedConfigurationSpringCloud.adoc`、`guide/cloud/cloudConfiguration/distributedConfigurationAwsParameterStore.adoc`、`guide/cloud/cloudConfiguration/distributedConfigurationOracleCloudVault.adoc`、`guide/cloud/cloudConfiguration/distributedConfigurationGoogleCloudSecretManager.adoc`、`guide/cloud/cloudConfiguration/distributedConfigurationKubernetes.adoc`、`guide/cloud/serviceDiscovery.adoc`、`guide/cloud/serviceDiscovery/serviceDiscoveryConsul.adoc`、`guide/cloud/serviceDiscovery/serviceDiscoveryEureka.adoc`、`guide/cloud/serviceDiscovery/serviceDiscoveryKubernetes.adoc`、`guide/cloud/serviceDiscovery/serviceDiscoveryRoute53.adoc`、`guide/cloud/serviceDiscovery/serviceDiscoveryManual.adoc`、`guide/cloud/clientSideLoadBalancing.adoc`、`guide/cloud/distributedTracing.adoc`、`guide/serverlessFunctions.adoc`、`guide/serverlessFunctions/awsLambda.adoc`、`guide/serverlessFunctions/gcpFunction.adoc`、`guide/serverlessFunctions/gcpCloudRun.adoc`

### B21（非代码词 2983 / 总词 3078）

`guide/serverlessFunctions/azureFunction.adoc`、`guide/messaging.adoc`、`guide/messaging/kafka.adoc`、`guide/messaging/rabbitmq.adoc`、`guide/messaging/nats.adoc`、`guide/commandLineApps.adoc`、`guide/commandLineApps/picocli.adoc`、`guide/configurations.adoc`、`guide/configurations/reactiveConfigs.adoc`、`guide/configurations/reactiveConfigs/reactor.adoc`、`guide/configurations/reactiveConfigs/rxjava3.adoc`、`guide/configurations/dataAccess.adoc`、`guide/configurations/dataAccess/sqlSupport.adoc`、`guide/configurations/dataAccess/hibernateSupport.adoc`、`guide/configurations/dataAccess/mongoSupport.adoc`、`guide/configurations/dataAccess/neo4jSupport.adoc`、`guide/configurations/dataAccess/postgresSupport.adoc`、`guide/configurations/dataAccess/redisSupport.adoc`、`guide/configurations/dataAccess/cassandraSupport.adoc`、`guide/configurations/dataAccess/liquibaseSupport.adoc`、`guide/configurations/dataAccess/flywaySupport.adoc`、`guide/logging.adoc`、`guide/logging/loggingMessages.adoc`、`guide/logging/loggingConfiguration.adoc`、`guide/logging/logback.adoc`、`guide/logging/loggingSystem.adoc`、`guide/languageSupport.adoc`、`guide/languageSupport/java.adoc`、`guide/languageSupport/java/java9.adoc`、`guide/languageSupport/java/incrementalannotationgradle.adoc`、`guide/languageSupport/java/lombok.adoc`、`guide/languageSupport/java/ide.adoc`、`guide/languageSupport/java/retainparameternames.adoc`、`guide/languageSupport/groovy.adoc`、`guide/languageSupport/python.adoc`

### B22（非代码词 3062 / 总词 3057）

`guide/languageSupport/python/pythonRuntime.adoc`、`guide/languageSupport/python/pythonThreading.adoc`、`guide/languageSupport/python/decorators.adoc`、`guide/languageSupport/python/sourceRoots.adoc`、`guide/languageSupport/python/typeOrdering.adoc`

### B23（非代码词 3378 / 总词 3353）

`guide/languageSupport/python/interfaces.adoc`、`guide/languageSupport/python/standardTypes.adoc`、`guide/languageSupport/python/javaCollections.adoc`、`guide/languageSupport/python/runtimeTypes.adoc`、`guide/languageSupport/python/javaImports.adoc`、`guide/languageSupport/python/keywords.adoc`

### B24（非代码词 3257 / 总词 3199）

`guide/languageSupport/python/nestedTypes.adoc`、`guide/languageSupport/python/pythonExceptions.adoc`、`guide/languageSupport/python/functionalInterfaces.adoc`、`guide/languageSupport/python/javaInterfaces.adoc`、`guide/languageSupport/python/generatedClasses.adoc`

### B25（非代码词 3096 / 总词 3070）

`guide/languageSupport/python/aopProxies.adoc`、`guide/languageSupport/python/extendingJavaClasses.adoc`、`guide/languageSupport/python/moduleScripts.adoc`、`guide/languageSupport/python/moduleScripts/testing.adoc`、`guide/languageSupport/python/graalTools.adoc`、`guide/languageSupport/python/asyncAwait.adoc`、`guide/languageSupport/python/asyncAwait/asyncioRuntime.adoc`

### B26（非代码词 3416 / 总词 3439）

`guide/languageSupport/python/asyncAwait/asyncioNetworking.adoc`、`guide/languageSupport/python/asyncAwait/asyncioStreaming.adoc`、`guide/languageSupport/python/asyncAwait/asyncioUnsupported.adoc`、`guide/languageSupport/kotlin.adoc`、`guide/languageSupport/kotlin/kaptOrKsp.adoc`、`guide/languageSupport/kotlin/kapt.adoc`、`guide/languageSupport/kotlin/ksp.adoc`、`guide/languageSupport/kotlin/controller.adoc`、`guide/languageSupport/kotlin/kaptintellij.adoc`、`guide/languageSupport/kotlin/gradlekapt.adoc`、`guide/languageSupport/kotlin/openandaop.adoc`、`guide/languageSupport/kotlin/kotlinretainparamnames.adoc`、`guide/languageSupport/kotlin/coroutines.adoc`、`guide/languageSupport/kotlin/coroutineTracingContextPropagation.adoc`

### B27（非代码词 3478 / 总词 3538）

`guide/languageSupport/kotlin/kotlinContextPropagation.adoc`、`guide/languageSupport/graal.adoc`、`guide/languageSupport/graal/graalServices.adoc`、`guide/languageSupport/graal/graalFAQ.adoc`、`guide/management.adoc`、`guide/management/buildingEndpoints.adoc`、`guide/management/buildingEndpoints/endpointAnnotation.adoc`、`guide/management/buildingEndpoints/endpointMethod.adoc`、`guide/management/buildingEndpoints/endpointSensitivity.adoc`、`guide/management/buildingEndpoints/endpointConfiguration.adoc`、`guide/management/providedEndpoints.adoc`、`guide/management/providedEndpoints/beansEndpoint.adoc`、`guide/management/providedEndpoints/infoEndpoint.adoc`、`guide/management/providedEndpoints/healthEndpoint.adoc`、`guide/management/providedEndpoints/healthEndpoint/healthEndpointConfiguration.adoc`、`guide/management/providedEndpoints/healthEndpoint/healthEndpointStatusCode.adoc`、`guide/management/providedEndpoints/healthEndpoint/healthLogging.adoc`

### B28（非代码词 2955 / 总词 3023）

`guide/management/providedEndpoints/healthEndpoint/healthEndpointCustomization.adoc`、`guide/management/providedEndpoints/healthEndpoint/healthMonitoringTask.adoc`、`guide/management/providedEndpoints/healthEndpoint/healthProvidedIndicators.adoc`、`guide/management/providedEndpoints/healthEndpoint/healthProvidedIndicators/diskSpaceHealthIndicator.adoc`、`guide/management/providedEndpoints/healthEndpoint/healthProvidedIndicators/jdbcHealthIndicator.adoc`、`guide/management/providedEndpoints/healthEndpoint/healthProvidedIndicators/discoveryClientHealthIndicator.adoc`、`guide/management/providedEndpoints/healthEndpoint/healthProvidedIndicators/deadlockedThreads.adoc`、`guide/management/providedEndpoints/metricsEndpoint.adoc`、`guide/management/providedEndpoints/refreshEndpoint.adoc`、`guide/management/providedEndpoints/routesEndpoint.adoc`、`guide/management/providedEndpoints/loggersEndpoint.adoc`、`guide/management/providedEndpoints/cachesEndpoint.adoc`、`guide/management/providedEndpoints/stopEndpoint.adoc`、`guide/management/providedEndpoints/environmentEndpoint.adoc`、`guide/management/providedEndpoints/threadDumpEndpoint.adoc`、`guide/security.adoc`、`guide/multitenancy.adoc`、`guide/cli.adoc`、`guide/cli/createProject.adoc`、`guide/cli/createProject/comparingVersions.adoc`、`guide/cli/features.adoc`

### B29（非代码词 3226 / 总词 3257）

`guide/cli/commands.adoc`、`guide/cli/reloading.adoc`、`guide/cli/reloading/automaticRestart.adoc`、`guide/cli/reloading/jrebel.adoc`、`guide/cli/reloading/gradleReload.adoc`、`guide/cli/reloading/ideReload.adoc`、`guide/cli/proxy.adoc`、`guide/i18n/bundle.adoc`、`guide/i18n/localizedMessageSource.adoc`、`guide/resources.adoc`、`guide/appendix/architecture.adoc`、`guide/appendix/architecture/compilerArch.adoc`、`guide/appendix/architecture/annotationArch.adoc`、`guide/appendix/architecture/introspectionArch.adoc`

### B30（非代码词 3387 / 总词 3401）

`guide/appendix/architecture/iocArch.adoc`、`guide/appendix/architecture/aopArch.adoc`、`guide/appendix/architecture/containerArch.adoc`、`guide/appendix/architecture/httpServerArch.adoc`

### B31（非代码词 955 / 总词 960）

`guide/appendix/faq.adoc`、`guide/appendix/usingsnapshots.adoc`、`guide/appendix/problems.adoc`

### B32（非代码词 3180 / 总词 3183）

`guide/appendix/breaks.adoc`、`guide/languageSupport/python/overloads.adoc`


---

*inventory 自动生成：scripts/inventory.py（PLAN §8；批次数以本报告实测为准）*