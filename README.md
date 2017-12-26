# LoadCombinations
This package is intended to generate lists of load combinations for structural
analysis.

The following taxonomy is used for the arrangement of load combinations:

1. ``Load``: The base element is a ``Load`` which corresponds to a specific
load (i.e. Dead Load, or Wind Load)
1. ``LoadGroup``: Loads are then combined into groups in a ``LoadGroup``. This
allows rules to be enforced such as 
"All the loads in this group are applied with the same factors" or 
"These loads rotate through a set of angles"
1. ``LoadCase``: Load groups are then combined into a ``LoadCase``, 
which corresponds to a design code Load Case (i.e. 1.2G + 1.5Q + 1.0Wu). Note 
tha G, Q & Wu correspond to specific ``LoadGroup`` objects, not necessarily to
specific ``Load`` objects. This allows cases where, for example, wind loads need
to be considered in say 4x different directions, to be specified as a single
``LoadCase`` object.
1. Finally, each ``LoadCase`` object will output a Load Combination consisting
of ``Load`` objects with their associated load factors, for each possible 
combination. This corresponds the real design combinations - for instance in the
1.2G + 1.5Q + 1.0Wu case listed above, if wind is specifid as 4x different load
cases (Wux, Wuz, Wu-x, Wu-z), the load combinations returned may be:
    * 1.2G + 1.5Q + 1.0Wux
    * 1.2G + 1.5Q + 1.0Wuz
    * 1.2G + 1.5Q + 1.0Wu-x
    * 1.2G + 1.5Q + 1.0Wu-z
