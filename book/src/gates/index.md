# Conditions and gates

“Activate this quest after X, Y, and Z” can describe several different engine
behaviors. This section separates them.

Planned control semantics:

- evaluate now and branch;
- wait until one condition is true;
- wait for every prerequisite;
- proceed when any prerequisite occurs;
- accept the first success, failure, timeout, or interruption;
- monitor a failure condition while another activity runs;
- require events in a specific order;
- choose an ordered or all-matching switch case;
- prevent re-entry or permit a controlled repeat.

Condition families include facts, journal state, time, triggers, distance,
inventory, characters, devices, vehicles, scenes, phones, content, scans,
destruction, spawning, and workspots.

The first gate lab will combine immediate conditions, pause conditions, logical
composition, a timeout race, and a persistent one-shot guard.
