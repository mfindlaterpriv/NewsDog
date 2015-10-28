# NewsDog
A library to analyze news sources, tallying references to specific information or countries.

NewsDog currently retreives results from Reddit, this will be optional in the very near future.
It also only currently tally references to countries, outputable as CSV.

Usage:

    import NewsDog
    
    # Create an object of NewsDog
    nd = NewsDog()
    
    # Analyze 100 results
    nd.analyze_day(limit=100)
    
    # Return CSV of data
    nd.geo_csv()
