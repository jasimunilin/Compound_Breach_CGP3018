# Compound Breach

First-person industrial escape prototype for Unreal Engine 5.8.

## Open and play

Open `Compound_Breach.uproject`. The startup map is `/Game/CompoundBreach/Maps/L_CompoundEscape`.
Press Play, then click the game viewport to give it keyboard and mouse focus.

Controls: WASD move, mouse look, Space jump, E interact, R restart.

## Escape route

1. Collect the yellow keycard from the desk inside A / Processing.
2. Activate the console beside the generator inside B / Generator.
3. Use the gate terminal inside C / Control.
4. Leave through the south exit gate.

The card and generator can be completed in either order. The control terminal needs both.
Ramps connect the upper walkway to the ground. The original starter map remains at `/Game/L_OriginalStarter`.

## Visual & Gameplay Features

- **Gameplay Assets:** `/Game/CompoundBreach/Blueprints` (`BP_EscapePlayer`, `BP_EscapeHUD`, `BP_EscapeGameMode`).
- **PBR Materials & Textures:** `/Game/CompoundBreach/Materials` and `/Game/CompoundBreach/Textures` (Concrete, Steel, Asphalt, Rust, Emissive indicators, Overcast Volumetric Clouds).
- **Industrial 3D Meshes:** `/Game/CompoundBreach/Meshes` (`SM_IndustrialCrate`, `SM_IndustrialDrum`, `SM_ServerRack`, `SM_Generator`, `SM_Terminal`, `SM_Door`), plus stepped staircases and catwalk safety rails.
- **Dynamic Power Lighting:** Activating the generator in Building B restores full interior illumination across all three compound buildings.
- **Standalone Build:** Download the packaged Windows release `.zip` from **GitHub Releases**, extract it, and run `Compound_Breach.exe` (press `Alt + F4` to exit).

