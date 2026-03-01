# q2fun

A Quake II deathmatch mod built on [Lithium II](https://github.com/mattayres/li2mod) and [Yamagi Quake II](https://github.com/yquake2/yquake2). Adds new gameplay features on top of the classic Lithium II rune/hook system.

## What is this?

q2fun is a server-side Quake II mod (`game.so`) that extends the Lithium II v1.32 mod with new content. It runs on the Yamagi Quake II dedicated server and is compatible with any Quake II client.

The Lithium II mod source was ported from the [original li2mod repository](https://github.com/mattayres/li2mod) to compile against the Yamagi Quake II game DLL codebase, which provides a modernized and maintained version of the id Software game source.

## Features

All standard Lithium II features are included:

- **Runes** (Resist, Strength, Haste, Regen, Vampire) that spawn on the map and grant special abilities
- **Grappling hook** with configurable behavior
- **Admin system** with menu-based remote administration
- **Map voting and map queue**
- **Configurable weapons, items, and gameplay variables**
- **HUD options** and player ID display
- **Anti-camping** system
- **High scores** tracking

### New: Predator Rune

A sixth rune inspired by the Aliens vs Predator Quake II mod:

| Ability | Description | Config var (default) |
|---------|-------------|---------------------|
| Cloaking | Player becomes translucent; breaks on firing, re-engages after delay | `rune_predator_recloak` (3.0s) |
| Speed boost | Faster movement | `rune_predator_speed` (1.3x) |
| Jump boost | Reduced gravity | `rune_predator_gravity` (0.65x) |
| Close-range damage | Bonus damage at short range | `rune_predator_closedmg` (2.0x) / `rune_predator_closerange` (100 units) |
| Self-destruct | Explosion on death damages nearby players | `rune_predator_selfdestruct_dmg` (200) / `_radius` (250) |

The Predator rune spawns with a dark grey shell and is included in the default rune rotation.

## Building

Requires GCC and GNU Make on Linux.

```bash
cd mod
make              # release build
make DEBUG=1      # debug build
make install      # install to ~/.yq2/lithium/
```

This produces `release/game.so` which is loaded by the Yamagi Quake II engine.

## Running

You need the Yamagi Quake II engine binary (`q2ded` for dedicated server or `quake2` for client) and the original Quake II game data (PAK files).

```bash
# Dedicated server
q2ded +set game lithium +set dedicated 1 +set deathmatch 1 +map q2dm1

# Local play
quake2 +set game lithium
```

## Project Structure

```
mod/
  src/
    game/          # Yamagi Quake II game DLL source (id Software, GPLv2+)
    lithium/       # Lithium II mod source (Matt Ayres, GPLv3+)
    common/        # Shared engine headers
  Makefile
engine/            # Yamagi Quake II engine source (not modified, not included in repo)
```

## License

This project contains code from multiple sources, all under GPL-compatible licenses:

- **Quake II game source** - Copyright (C) 1997-2001 Id Software, Inc. Licensed under the GNU General Public License v2 or later.
- **Lithium II Mod** - Copyright (C) 1997, 1998, 1999, 2010 Matthew A. Ayres. Licensed under the GNU General Public License v3 or later.
- **Yamagi Quake II** modifications to the game source - Licensed under the GNU General Public License v2.

The combined work is distributed under the **GNU General Public License v3**. See [LICENSE](LICENSE) for the full license text.

### Acknowledgments

- [Matt "WhiteFang" Ayres](https://quake2lithium.github.io/) for the Lithium II mod
- [Id Software](https://www.idsoftware.com/) for Quake II and releasing the source under GPL
- [Yamagi Quake II](https://www.yamagi.org/quake2/) team for the modernized engine and game source
