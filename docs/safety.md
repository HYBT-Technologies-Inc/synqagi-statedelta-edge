# Safety Architecture

The decision model is advisory. Final physical authority belongs to deterministic validation.

The validator must:

- enforce an action whitelist;
- verify evidence requirements;
- apply hard safety rules;
- reject malformed commands;
- choose a safe fallback when evidence is insufficient;
- prevent model output from overriding emergency limits.

Low-level PWM, voltage, current, motor timing, braking, and emergency-stop logic must remain outside the language-model control loop.
