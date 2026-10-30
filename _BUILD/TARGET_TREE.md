# TARGET CANONICAL ARCHITECTURE

End-state of the Python package (repo_root/uro/). Everything else is
consolidated into this tree or deleted. Rendered as 4-space-indented text
(no markdown fences) to keep payloads chat-fence-safe.

    uro/
    ├── __init__.py            # canonical exports only; no _CompatStub
    ├── constants.py           # bit widths, baselines, epoch, currency ratios
    ├── exceptions.py          # typed URO exception hierarchy
    ├── types.py               # shared aliases / Protocols
    ├── core/                  # urid.py uro.py header.py components.py
    │   │                      # inheritance.py datetime_uro.py
    ├── nte/                   # axes.py state.py cross_talk.py polarity.py
    │   │                      # math_influence.py firing.py reward.py ans.py
    ├── synapse/               # vector.py engine.py persistence.py __init__.py
    ├── opar/                  # base.py protocol.py stages.py grounding.py compliance.py
    ├── coordinator_bus.py     # auto synapse create/modulate on emit/await
    ├── quad/                  # quad_capability.py croate.py character_condition.py
    ├── security/              # inahash.py encryption.py pki.py identity.py acl.py
    │   │                      # policy.py circle_security.py field_encryption.py
    │   │                      # custody.py ldap.py
    ├── memory/                # hierarchy.py movement.py consolidation.py sleep.py
    ├── pathing/               # pathing.py associations.py cro_matrix.py trust_value.py
    │   │                      # beacons.py resolution.py onion.py path_ops.py
    │   │                      # connectors.py swarms.py
    ├── interchange/           # upi.py aupi.py interchange.py self_loading.py priority.py
    ├── learning/              # primitives.py pattern.py action_uros.py attention.py
    │   │                      # companion.py robotics.py sensory.py wetware.py
    ├── hardware/              # chip_arch.py asic_specs.py drivers.py (simulation only)
    ├── boot/                  # boot_sequence.py child_boot.py self_check.py
    ├── economy/               # currency.py token_transfer.py marketplace.py
    │   │                      # social_pricing.py supply_chain.py
    ├── docks/                 # dock.py manifest.py registry.py interceptor.py dock_defs/
    ├── ecosystem/             # api/ connectors/ api_creator.py
    ├── invariants.py          # ten invariants as runtime assertions
    └── glossary.py            # glossary as structured data
