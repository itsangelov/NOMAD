# NOMAD

A portable, self-contained, offline-first field computer.

> **Assume the infrastructure is gone.**

NOMAD carries its own computing, storage, offline knowledge, maps, GNSS navigation, local AI, communications, display, controls and power, with future battery and deployable solar generation. It is meant to be a working field computer, not a decorative cyberdeck.

## Status

**Phase:** NOMAD V1 — Mechanical Architecture & Chassis Engineering
**Current prototype:** P0.1 — mechanical proof of concept (not yet modeled)

## Baseline hardware (provisional)

| Subsystem | Baseline |
|---|---|
| Computer | Raspberry Pi 5, 8 GB |
| Storage | 500–512 GB NVMe (2230 preferred) via Raspberry Pi M.2 HAT+ |
| Display | 10.1" IPS, 1920×1200, 16:10, ≥400 nit, matte, HDMI (SKU not locked) |
| Keyboard | Ultra-low-profile wired USB HID, ~280×105 mm (SKU not locked) |
| Trackpad | Perixx PERIPAD-501 II (candidate) |
| GNSS | SparkFun GNSS Flex pHAT / DAN-F10N (candidate) |
| Power | Ready-made modules; battery sized from measured consumption |
| Solar | Two deployable sliding/rotating solar cassettes |

## Repository layout

| Path | Contents |
|---|---|
| `docs/` | Engineering specifications, decisions, build log |
| `CAD/` | Derived CAD outputs and FeatureScript snapshots (Onshape is the master) |
| `hardware/` | Electronics, power, GNSS, sensors |
| `software/` | Launcher, maps, navigation, knowledge, AI, power, system |
| `prototypes/` | Per-prototype notes, test results, photos |
| `media/` | Photos and videos |

## Sources of truth

- **Parametric CAD:** Onshape. Exported STEP/STL/3MF files are derived outputs.
- **Specifications:** `docs/`
- **Decisions:** `docs/decisions.md`
- **Build history:** `docs/build-log.md`
