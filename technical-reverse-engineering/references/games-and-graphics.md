# Games and graphics API usage

Use this guide when the target is a game or another program whose behavior is
mostly visible through what it draws, plays, and reads from asset files. The
graphics API is the most useful landmark in such a program: it is documented,
it is called at known points in every frame, and each call names the data
passed to it. Tracking those calls leads back to the renderer, the main loop,
the asset loaders, and the game state.

## Scope

Work on software the user is authorized to analyze, for interoperability,
preservation, modding of single-player content, porting, or documentation.
Do not use these techniques to defeat anti-cheat, DRM, licensing, or the
protections of an online service, or to build cheats for multiplayer games.
If a request needs that, say so and stop at what can be done without it.

## Identify the stack

Start from imports, bundled DLLs, and strings. They usually name the API
generation, which sets everything else.

| Evidence | API | Era and notes |
|---|---|---|
| `INT 10h` mode sets, writes to `A000:0000`, ports `3C4h`-`3C9h` | VGA, Mode X, VESA | DOS. See [DOS and 16-bit Windows](dos-and-win16.md) |
| `glide2x.dll`, `glide3x.dll`, `grSstWinOpen`, `grBufferSwap` | 3dfx Glide | 1996-2000 |
| `ddraw.dll`, `DirectDrawCreate`, `DirectDrawCreateEx` | DirectDraw | DirectX 1-7. Also the route to Direct3D before version 8 |
| `d3drm.dll` | Direct3D Retained Mode | DirectX 2-6 |
| `d3d8.dll` `Direct3DCreate8`, `d3d9.dll` `Direct3DCreate9` | Direct3D 8 / 9 | 2000-2010 |
| `d3d11.dll` `D3D11CreateDevice`, `dxgi.dll` | Direct3D 10 / 11 | DXGI swap chain presents |
| `d3d12.dll` `D3D12CreateDevice` | Direct3D 12 | Command lists and queues |
| `opengl32.dll`, `wgl*`, `glX*`, `egl*` | OpenGL / GLES | Any era; see below |
| `vulkan-1.dll`, `vkCreateInstance` | Vulkan | |
| `dsound.dll`, `dinput.dll`, `dinput8.dll`, `dplayx.dll`, `xinput*.dll` | DirectSound, DirectInput, DirectPlay, XInput | Audio, input, network |
| `SDL*.dll`, `glfw`, `allegro`, `bgfx`, `sokol` | Wrapper libraries | The real API is underneath; find which backend was built in |

Middleware explains large parts of a binary that are not worth reading:
Miles Sound System (`mss32.dll`, `AIL_` functions), Bink and Smacker video
(`binkw32.dll`, `smackw32.dll`), FMOD, Havok, PhysX, Scaleform, and embedded
scripting (`Lua 5.x` strings and `lua_`/`luaL_` names, Python, Squirrel).
Identify these first and treat them as libraries.

An engine changes the whole approach. Unity ships managed assemblies or an
IL2CPP `GameAssembly`; Unreal, id Tech, Source, and GameMaker each have known
package formats and community documentation. Name the engine and version
before reading any code, and use the route for that kind of target (managed,
native, or script) from `SKILL.md`.

## DirectX: calls go through COM tables

Only the creation functions are imports. Everything after that is a call
through an interface pointer:

```
mov  eax, [device]        ; interface pointer
mov  ecx, [eax]           ; its vtable
call [ecx + 0xA8]         ; slot 0xA8 / 4 = 42
```

To name those calls:

1. **Find creation.** Cross-reference the import (`DirectDrawCreate`,
   `Direct3DCreate9`, `D3D11CreateDeviceAndSwapChain`, `DirectSoundCreate`,
   `DirectInput8Create`, `CoCreateInstance`). The out-parameter is where the
   interface pointer is stored; that global or struct field is what every
   later call loads.
2. **Know which interface the pointer is.** `QueryInterface` and
   `CoCreateInstance` take an interface ID, a 16-byte GUID stored in the
   binary (first field little-endian, so `{6C14DB80-A733-11CE-...}`,
   `IID_IDirectDraw`, begins `80 DB 14 6C`). Searching the data for known IIDs
   shows which interface versions the program uses. Early Direct3D is reached
   this way: the program queries its DirectDraw object for `IDirect3D`,
   `IDirect3D2`, `IDirect3D3`, or `IDirect3D7`.
3. **Map slot to method from the SDK header.** Slot index is the method's
   position in the interface declaration, counting inherited methods first
   (`IUnknown` occupies 0-2: `QueryInterface`, `AddRef`, `Release`). Take the
   order from the header for that exact interface version (`ddraw.h`,
   `d3d.h`, `d3d8.h`, `d3d9.h`, `d3d11.h`, `dxgi.h`), because later versions
   insert methods. State the header and version you used.

Anchors worth knowing, to check a mapping against (32-bit offset is slot x 4,
64-bit is slot x 8):

| Interface | Slot | Method |
|---|---|---|
| `IDirectDraw` | 6, 20, 21 | `CreateSurface`, `SetCooperativeLevel`, `SetDisplayMode` |
| `IDirectDrawSurface` | 5, 7, 11, 25, 32 | `Blt`, `BltFast`, `Flip`, `Lock`, `Unlock` |
| `IDirect3DDevice9` | 16, 17, 41, 42, 43 | `Reset`, `Present`, `BeginScene`, `EndScene`, `Clear` |
| `IDirect3DDevice9` | 23, 65, 81, 82 | `CreateTexture`, `SetTexture`, `DrawPrimitive`, `DrawIndexedPrimitive` |
| `IDXGISwapChain` | 8, 13 | `Present`, `ResizeBuffers` |
| `ID3D11DeviceContext` | 12, 13 | `DrawIndexed`, `Draw` |

`scripts/capstone_scan.py vcalls` lists every `call [reg + disp]` with its
slot (see [scripted disassembly](scripted-disassembly.md)). A slot number
alone does not identify the interface: confirm what object the register holds
at that site before naming the call. Slots that recur thousands of times with
small indices are usually `Release` and `AddRef`.

## OpenGL: calls are named, extensions are strings

- Core functions are ordinary imports from `opengl32.dll` (or `libGL`), so
  cross-references to `glBegin`, `glDrawElements`, `glTexImage2D`, and
  `glBindTexture` work directly.
- Context setup is platform code: `ChoosePixelFormat`, `SetPixelFormat`,
  `wglCreateContext`, `wglMakeCurrent` on Windows; `glXCreateContext` or
  `eglCreateContext` elsewhere. The frame ends at `SwapBuffers` /
  `wglSwapBuffers`, `glXSwapBuffers`, or `eglSwapBuffers`.
- Anything newer than OpenGL 1.1 on Windows is fetched at run time with
  `wglGetProcAddress` (or through GLEW, GLAD, SDL). The function names are
  strings in the binary (`glActiveTextureARB`, `glCreateShader`); the result
  is stored in a table of function pointers and called indirectly. Find the
  loader, name the table entries from the strings, and the indirect calls
  become readable.
- The call style dates the renderer: `glBegin`/`glVertex` immediate mode and
  display lists, then vertex arrays and `ARB` assembly programs
  (`!!ARBvp1.0`), then buffers and GLSL.
- A game directory containing its own `opengl32.dll` from the late 1990s is
  often a MiniGL driver that translates to Glide; the real renderer is still
  the game's OpenGL calls.

## Shaders and GPU data

- GLSL is usually plain text in the binary or in asset files, passed to
  `glShaderSource`.
- Direct3D 9 bytecode starts with a version token (`0xFFFE0300` for
  `vs_3_0`, `0xFFFF0300` for `ps_3_0`) and is passed to `CreateVertexShader`
  or `CreatePixelShader`. Direct3D 10 and later use a container starting
  `DXBC`. Both disassemble with the SDK's `fxc /dumpbin` or `D3DDisassemble`.
- HLSL source may be present instead, compiled at run time through
  `D3DCompile` or `D3DXCompileShader`.
- SPIR-V modules start with `0x07230203`.
- Fixed-function Direct3D describes vertices with an FVF code
  (`D3DFVF_XYZ` is `0x002`, `D3DFVF_NORMAL` `0x010`, `D3DFVF_DIFFUSE`
  `0x040`, `D3DFVF_TEX1` `0x100`), later with a vertex declaration; OpenGL
  with `glVertexPointer`-family strides or attribute bindings. These give the
  in-memory vertex layout, which is usually close to the on-disk mesh format.

## Observing calls at run time

Static cross-references say where an API is used. A trace says in what order,
with what arguments, and how often per frame. Follow
[runtime observation](runtime-observation.md) for REA's own instrumentation
and its launch, attach, and cleanup rules; the tools below are outside REA and
their output is your own observation.

| Tool | Covers | Notes |
|---|---|---|
| apitrace | OpenGL, Direct3D 8-11, DirectDraw | Records every call with arguments to a file that can be replayed and inspected frame by frame |
| RenderDoc | Direct3D 11/12, Vulkan, modern OpenGL | Frame capture with draw-call list, resources, pipeline state, and optional call stacks |
| PIX | Direct3D 11/12 | Microsoft's capture and timing tool |
| Wine debug channels | DirectDraw and all Direct3D, on Linux | `WINEDEBUG=+ddraw,+d3d` logs calls with no change to the game |
| Translation layers | Old APIs to modern ones | dgVoodoo 2 (Glide, DirectDraw, Direct3D up to 8), DXVK (Direct3D 8-11 to Vulkan), d3d8to9. Put one under an old game and capture the translated output with a modern tool |
| Proxy DLL | Any API loaded from the game directory | A `ddraw.dll`, `d3d9.dll`, `opengl32.dll`, or `dinput.dll` that logs and forwards. Changes the process; use on a copy |
| DOSBox debugger, DOSBox-X | DOS games | Breakpoints on interrupts, port I/O, and memory writes to video memory |

Run captures in an isolated environment on a copy of the game. A trace file
contains the game's textures, models, and shaders; treat it as the game's
content when sharing it.

## Using the calls as landmarks

The point of tracking graphics calls is what they lead back to.

- **Main loop.** The caller of the frame-end call (`Present`, `Flip`,
  `SwapBuffers`, `grBufferSwap`, `vkQueuePresentKHR`) is the render function;
  its caller is the main loop. Timing calls near it (`timeGetTime`,
  `QueryPerformanceCounter`, `GetTickCount`) show the update step and whether
  it is fixed.
- **Asset loaders.** Texture creation followed by an upload (`Lock`/`Unlock`,
  `LockRect`, `UpdateSubresource`, `glTexImage2D`) receives decoded pixels with
  explicit width, height, and format. Follow the pixel pointer backwards to
  the decoder, and the decoder's input back to the file read. The same works
  from vertex-buffer fills to mesh loaders and from DirectSound or mixer
  buffer writes to audio decoders.
- **Camera and transforms.** `SetTransform` with the world, view, or
  projection selector, `glLoadMatrixf`, or a uniform or constant-buffer upload
  receives matrices. Their sources are the camera and object transforms in
  game state.
- **Render passes.** Runs of state changes and target switches between draws
  mark passes (world, sprites, UI, post-processing). Name functions after the
  pass they issue.
- **UI and text.** Text and sprite draws with recognizable string or atlas
  arguments lead to menu and HUD code, which reads the game state it displays
  (health, score, inventory).
- **Input.** `GetDeviceState` and `GetDeviceData` (DirectInput), `XInputGetState`,
  `GetAsyncKeyState`, or the keyboard interrupt handler in DOS lead to the
  input mapping and from there to player actions.

## Game-specific structure

- **Archives.** Most games pack assets. Check magic bytes before reverse
  engineering a format that is already documented: `IWAD`/`PWAD` (Doom),
  `PACK` (Quake), `PK\x03\x04` (ZIP, including `.pk3`), `MPQ\x1A` (Blizzard),
  `BIGF` (EA), `KenSilverman` (Build `.GRP`), `RIFF`, `DDS `, `BIK`/`SMK2`
  video, `SCRM` and `M.K.` tracker music, `Creative Voice File`. Compression
  inside is commonly zlib (`78 9C`, `78 DA`), LZSS, RLE, LZO, or `RNC`.
- **Unknown formats.** Find the loader from file-open calls and the path or
  extension strings, read its header parsing, and confirm against several real
  files. Report fields you have confirmed separately from fields you inferred.
- **Fixed-point math.** Older games avoid floating point: 16.16 values show as
  multiplies followed by 16-bit shifts (`imul` then `shrd`), with sine and
  reciprocal lookup tables in data.
- **Random numbers.** Linear congruential constants identify the generator
  (`0x343FD` and `0x269EC3` for Microsoft C `rand`, `1103515245` and `12345`
  for the ANSI example). Its call sites are the game's chance-based logic.
- **Script interpreters.** A loop that reads a byte or word, indexes a jump
  table, and dispatches is a virtual machine. The game logic is then in the
  script data, and the work shifts to documenting the opcodes.
- **State.** Game state lives in a few large structures or arrays. Recover
  layouts from access patterns in code that displays or saves them; save-file
  writers serialize exactly the state that matters.
- **Reproducibility.** Use save files, built-in demo playback, a fixed random
  seed, or emulator save states so the same code path can be observed twice.
  An observation that cannot be repeated is weak evidence.

## Reporting

Follow [evidence workflows](evidence-workflows.md). For these targets, state
in addition:

- the graphics, audio, and input APIs and versions, and what identified them;
- the engine and middleware, with the evidence;
- for each named COM call: the interface, the header and version the slot
  mapping came from, and how the object's type at that site was established;
- which findings are static and which came from a trace or capture, naming
  the tool, its version, and any translation layer or proxy in between;
- for file formats: which fields were checked against real files and how many.
