# route-solver

This code originated from a homework assignment in one of my grad-school classes. It has some problems. I work on it for fun from time to time.

To run the code:

    $> python3 runner.py --start Madison,_Indiana --end Chicago,_Illinois --opt distance

Note the underscores where you would normally have a space. Also, state names are always spelled out.

The --opt flag specifies the optimization function. Choices are:

    * segments.......... Find the minimum number of connecting roads.
    * distance.......... Find the shortest distance.
    * time.............. Find the minimum travel time.
    * accidents......... Fine the minimum probability of an accident involving a bicycle.
    
Example output:

    ********* ROUTE SOLVER STARTING *********
    Searching for route between Madison, Indiana and Chicago, Illinois.
    Optimizing for shortest distance.
    Found solution in 0.2169 seconds.
    SOLUTION:
      Road segments:	24
      Distance: 	465.0 miles
      Travel Time:	8.3988 hours
      Expected cycling accidents: 0.024016
      Connecting cities:
        Madison,_Indiana
        North_Vernon,_Indiana
        Columbus,_Indiana
        Franklin,_Indiana
        Martinsville,_Indiana
        Bloomington,_Indiana
        Spencer,_Indiana
        Romona,_Indiana
        Cloverdale,_Indiana
        Morton,_Indiana
        Crawfordsville,_Indiana
        Rockville,_Indiana
        Montezuma,_Indiana
        Covington,_Indiana
        Danville,_Illinois
        Champaign,_Illinois
        Gilman,_Illinois
        Ashkum,_Illinois
        Kankakee,_Illinois
        Joliet,_Illinois
        Bolingbrook,_Illinois
        Crest_Hill,_Illinois
        Aurora,_Illinois
        Lisle,_Illinois
        Hillside,_Illinois
        Chicago,_Illinois
    ********* ROUTE SOLVER FINISHED *********


