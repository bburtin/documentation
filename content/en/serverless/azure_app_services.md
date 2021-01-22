---
title: Microsoft Azure App Services Extension
kind: documentation
aliases:
  - /infrastructure/serverless/azure_app_services/
further_reading:
- link: "/integrations/azure_app_services/"
  tag: "Documentation"
  text: "Azure App Service"
- link: "/integrations/azure_app_service_environment/"
  tag: "Documentation"
  text: "Azure App Service Environment"
---

## Overview

Microsoft Azure App Services is a group of serverless resources that enable you to build and host web apps, mobile back ends, event-driven functions, and RESTful APIs without managing infrastructure. It can host workloads of all sizes and offers auto-scaling and high availability options.

Datadog provides monitoring capabilities for all Azure App Services resource types:

- Azure Monitor metrics for [Apps][1] and [Functions][2] using the [Azure Integration][1].
- Custom metrics can be submitted using the API.
- [Resource logs][3] can be submitted using [Event Hub][4].

The Datadog extension for Azure App Services provides additional monitoring capabilities for [Azure Web Apps][5]. This support includes:

- Full distributed APM tracing using automatic instrumentation.
- Support for manual APM instrumentation to customize spans.
- `Trace_ID` injection into application logs.
- Support for submitting custom metrics using [DogStatsD][6].

## Setup

### Requirements

If you haven't already, set up the [Microsoft Azure integration][7] first.

The Datadog .NET APM extension supports the following .NET runtimes in both x64 and x86 architectures when running on Windows instances (AAS does not yet support extensions on Linux). For more details about automatically instrumented libraries, see the [Tracer documentation][8].

- .NET Framework 4.7 and later
- .NET Core 2.1
- .NET Core 2.2 (Microsoft support ended 2019-12-23)
- .NET Core 3.0 (Microsoft support ended 2020-03-03)
- .NET Core 3.1

Datadog recommends doing regular updates to the latest version of the extension to ensure optimal performance, stability, and availability of features.

### Installation

1. Configure the Azure integration to monitor your web app and verify it is configured correctly by ensuring that you see an `azure.app_service.count` metric tagged with the name of your web application. **Note**: This step is critical for metric/trace correlation, functional trace panel views in the Datadog portal, and accurate billing.

2. Open the [Azure Portal][9] and navigate to the dashboard for the Azure App Services instance you wish to instrument with Datadog.

3. Go to the Application settings tab of the Configuration page.
    {{< img src="infrastructure/serverless/azure_app_services/config.png" alt="configuration page" >}}
4. Add your Datadog API key as an application setting called `DD_API_KEY` and a value of your [Datadog API Key][10].
    {{< img src="infrastructure/serverless/azure_app_services/api_key.png" alt="api key page" >}}
5. Configure optional application settings:
    - Set the `DD_SITE` to `{{< region-param key="dd_site" code="true" >}}` (defaults to `datadoghq.com`).
    - Set `DD_ENV` to group your traces and custom statistics.
    - Set `DD_SERVICE` to specify a service name (defaults to your web app name).
    - Set `DD_LOGS_INJECTION:true` for correlation with application logs from your web app.
    - See a full list of [optional configuration variables][11].
6. Go to the extensions page and click **Add**.
7. Select the Datadog APM extension.
    {{< img src="infrastructure/serverless/azure_app_services/extension.png" alt="Datadog extension" >}}
8. Accept the legal terms, click **OK**, and wait for the installation to complete.
9. Restart the main application: click **Stop**, wait for a full stop, then click **Start**.
    {{< img src="infrastructure/serverless/azure_app_services/restart.png" alt="Stop and restart page" >}}

### Application logging from Azure Web Apps

Sending logs from your application in Azure App Services to Datadog requires the use of Serilog. Submitting logs with this method allows for trace ID injection, which makes it possible to connect logs and traces in Datadog. To enable trace ID injection with the extension, add the application setting `DD_LOGS_INJECTION:true`.

**Note**: Since this occurs inside your application, any Azure Platform logs you submit with diagnostic settings does not include the trace ID.

See documentation on [setting up agentless logging with Serilog][12] for detailed instructions.

## Custom metrics with DogStatsD

The App Services extension includes an instance of [DogStatsD][6] (Datadog's metrics aggregation service). This enables you to submit custom metrics, service checks, and events directly to Datadog from Azure Web Apps with the extension.

Writing custom metrics and checks in your web app is similar to the process for doing so with an application on a host running the Datadog Agent. To submit custom metrics to Datadog from Azure App Services using the extension:

1. Add the [DogStatsD NuGet package][13] to your Visual Studio project.
2. Initialize DogStatdD and write custom metrics in your application.
3. Deploy your code to a supported Azure .NET web app.
4. Install the Datadog App Service extension.

**Note**: Unlike the [standard DogStatsD config process][14], there is no need to set ports or a server name when initializing the DogStatsD configuration. There are ambient environment variables in Azure App Service that determine how the metrics are sent (requires v6.0.0+ of the DogStatsD client).

To send metrics use this code:

```csharp
using (var statsService = new DogStatsdService())
{
    statsService.Configure(new StatsdConfig());
    // Submit any metrics here:
    statsService.Increment("your.metric");
}
```


Learn more about [custom metrics][15].

## Troubleshooting

Need help? Contact [Datadog support][16].

To expedite the process of investigating application errors, consider setting `DD_TRACE_DEBUG:true` and adding the content of the Datadog logs directory (`%AzureAppServiceHomeDirectory%\LogFiles\datadog`) to your email.

### Further Reading

{{< partial name="whats-next/whats-next.html" >}}


[1]: /integrations/azure_app_services/
[2]: /integrations/azure_functions/
[3]: https://docs.microsoft.com/en-us/azure/azure-monitor/platform/resource-logs
[4]: /integrations/azure/?tab=eventhub#log-collection
[5]: https://azure.microsoft.com/en-us/services/app-service/web/
[6]: /developers/dogstatsd
[7]: /integrations/azure
[8]: /tracing/setup/dotnet/
[9]: https://portal.azure.com
[10]: https://app.datadoghq.com/account/settings#api
[11]: /tracing/setup_overview/setup/dotnet-framework/#additional-optional-configuration
[12]: /logs/log_collection/csharp/?tab=serilog#agentless-logging
[13]: https://www.nuget.org/packages/DogStatsD-CSharp-Client
[14]: /developers/dogstatsd/?tab=net#code
[15]: /developers/metrics/
[16]: /help
