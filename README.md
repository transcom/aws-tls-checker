# Description

This AWS Lambda function written in Python checks the SSL expiration date of a list of hostnames and notifies via an AWS SNS topic if any of the SSLs are expiring within a specified number of days. It uses the python built-in libraries ssl and socket to establish a connection with the hostname over a SSL and check the certificate expiration date.

The function accepts a list of dictionaries containing hostname, port, and days_to_notify values, and loops through the list, for each host it establish a connection, get the certificate, parses the expiration date and calculates the remaining time until expiration in seconds.
It then compares the remaining time until expiration to the days_to_notify value, if it is less or equal it sends a message containing the hostname and remaining days to the specified SNS topic.

It uses print statements to log the expiration date of each host, and in case of any error it will log the error message with the hostname it was checking at the time.
This function allows the user to specify a list of hosts that need to be checked and the number of days before expiration to be notified. It is useful to ensure that the SSL certificate of an online service or internal systems are up-to-date, and to automate the process of renewing the SSL certificate before it expires.

## Building a new version

You will want to edit the source files for this Lambda in the ./src
directory. Once you are ready to build a new release package you can do
the following:

`./build.sh`

The build script will ask you the version number you would like to build
and create a release package (.zip) in the main directory with that version
in the file name.

## Tracking changes to source

After a release it is highly recommended that you commit your changes to
the repo. You can revert a previous commit if you would like to build a
previous version.

