# Konula
<a href="#" alt="test version">
    <img alt="test" src="https://img.shields.io/badge/version-0.0.1-red.svg?color=0052FF&labelColor=090422">
</a>
 
<a href="#" alt="test version">
    <img alt="test" src="https://img.shields.io/badge/stage-alpha-red.svg?color=0052FF&labelColor=090422">
</a>

<!-- <a href="https://pypi.python.org/pypi/sqlalchemy/" alt="PyPI version">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/sqlalchemy?color=0052FF&labelColor=090422">
</a> -->

See checklist for alpha release [here](https://github.com/sccox/konula/blob/master/alpha_checklist.md)

### What problem are we solving?
It is difficult to establish clear data quality and integrity practices, and even more difficult when multiple systems manage key elements of a dataset.
Konula aims to provide a clear roadmap for monitoring data and integrity, along with the systems that provide and manipulate that data.

## How are we solving it? 
Konula provides 3 ways to manage data system integrity:
- Validate data at rest
- Validate data in transit
- Validate data management systems (applications, pipeline metrics)

## How does Konula work?
Konula has 3 main components including:
- A cloud-only user interface and API for managing checks, scheduling, secrets, logs, notifications and workflows
- An open source package the houses all of the code needed to run Konula in the cloud and locally
- An open source helm chart to handle the kubernetes deployment so that you can run checks on your infrastructure (we don't handle those right now, and most clients want to run on their infrastructure for security)

## Creating Checks
### How can I build Checks with Konula?
- **Core Check** - a check created in the UI, configured to use existing connectors, and executed by your k8s Konula Runner.
- **Remote Check** - a check created in the UI, configured based on existing connectors, and executed by your script.
- **Local Check** - a check independent from the UI, configured in a local script, and executed by that script, with no incoming or outgoing communication with the API.

### Core Check
#### Explained
The core check is a feature intended for running critical comparisons and key data validations on **existing and filtered datasets**. Core checks are created strictly in the UI, and are executed on your kubernetes instance as a job. Core tests are more simple to create and easier to manage. When creating a data check, core checks are highly recommended!
#### Example
An example of a core check would be running a comparison on the opportunity data in your teams Redshift warehouse with the opportunity data in your Salesforce instance. You could run column-by-column comparisons, or look for a match on the maximum last modified date. You could also run core checks on one of those datasources by filtering and aggregating relevant ACV totals or looking for QR percentages that need attention. 

### Remote Check
#### Explained
The remote check is a feature intended for running comparisons and validations on in-transit datasets. There are some tests that won't be able to be covered by core checks, because you need to react to issues while the data is still in-transit, the checks do not yet exist -[contribute here!!]()- or because your specific test or workflow does not fit into the patterns available. Remote checks can use core connectors if needed. Results will still be tracked in the API, and workflow triggers will still be configurable.
#### Example
An example of a remote check would be running a comparison on two pandas/spark dataframes, or running a custom ML model and validating the output.  

### Local Check
#### Explained
The local check is a feature intended for running local comparisons and validations without interaction with the api. No API connection is required, and results can be handled in whatever way you need. This option will ALWAYS BE FREE and simply requires installation of the package.  Local checks can also be used to test remote checks without interacting with the API. Remember, local checks do not come with many of the incredible workflow triggers, trend monitoring, health metrics, and alert based-reporting that Remote and Core checks offer. Remember, remote and core checks can be used with free tier!
#### Example
An example of a local check would be running a comparison on a pandas dataframe, then manually performing an action based on the check response. 

## Check Types
See current check types [here](https://github.com/sccox/konula/tree/master/main/package/src/checks)



# Checklist for 0.0.1 - OS release

Core
- [x] Basic core configuration and connection to remote API
- [x] Cleanup local checks
- [x] Check error handling
- [ ] Make sending a check really simple from a coding standpoint

Connectors
- [ ] Add custom query support for database connectors
- [ ] Add sqlalchemy connector for users that want to provide their own engine
- [ ] Clear documentation for connection and use
- [ ] Instructions for adding secrets from a remote run
- [ ] Clear documentation for creating a new connector
- [ ] Website pull recent verion of package and connector statuses
- [ ] Automatic testing for connectors, clear documentation for connecting to the testing framework

Workflows
- [ ] Core workflow/integration creation documentation
- [ ] core workflow configuration
- [ ] Slack workflow
- [ ] Email workflow
- [ ] Remote store results - S3 (destination connector)

API - Not needed for OS release
- [ ] Create basic API and have everything functional
- [ ] Payment process and user run tracking in place


WebApp
- [ ] Community pages, slack, discord, stackoverflow tags
- [ ] Simple web page with links to documentation, videos, project overview, plan moving forward
