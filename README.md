# hello-lambda
Serverless random greeting generator: https://hello.emshea.com/

When invoked by an HTTP request, GreetingsFunction sends a list of possible greetings and a list of possible font colors to the RandomEntrySelector function. The RandomEntrySelector responds with a random entry from both lists. The GreetingsFunction inserts these entries in the webpage HTML. 

The GreetingsFunction also calls a current weather data API - the default location is Seattle but users can pass a new location to the weather data API using query string paramaters.

Example: https://hello.emshea.com/?l=Portland

