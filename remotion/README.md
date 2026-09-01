# Remotion video

<p align="center">
  <a href="https://github.com/remotion-dev/logo">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://github.com/remotion-dev/logo/raw/main/animated-logo-banner-dark.apng">
      <img alt="Animated Remotion Logo" src="https://github.com/remotion-dev/logo/raw/main/animated-logo-banner-light.gif">
    </picture>
  </a>
</p>

Welcome to your Remotion project!

## Nota de ARION_OS

En el entorno de nube donde vive este repo, `node sub.mjs` (descarga de
Whisper.cpp) está bloqueado por política de red (mismo problema que
`faster-whisper` en `video_engine/`). Este template se usa como **motor
de render de subtítulos animados**, no de transcripción, en ese entorno.

Flujo recomendado:

1. Transcribe con `python3 scripts/edit_video.py <video>` en una máquina
   con internet sin restricciones (tu Mac) — genera `edl.json` con
   timestamps por palabra.
2. Convierte a formato Remotion:
   `python3 scripts/edl_to_remotion_captions.py <edl.json> remotion/public/<nombre>.json`
3. Copia el video a `remotion/public/<nombre>.mp4` (mismo nombre base
   que el `.json`).
4. `npm run dev` para previsualizar, `npx remotion render` para exportar.

Si tu Mac tiene acceso completo a internet, `node sub.mjs` también
funciona de forma autónoma sin pasar por el pipeline de Python.

## Commands

**Install Dependencies**

```console
npm i
```

**Start Preview**

```console
npm run dev
```

**Render video**

```console
npx remotion render
```

**Upgrade Remotion**

```console
npx remotion upgrade
```

## Captioning

Replace the `sample-video.mp4` with your video file.
Caption all the videos in you `public` by running the following command:

```console
node sub.mjs
```

Only caption a specific video:

```console
node sub.mjs <path-to-video-file>
```

Only caption a specific folder:

```console
node sub.mjs <path-to-folder>
```

## Configure Whisper.cpp

Captioning will download Whisper.cpp and the 1.5GB big `medium.en` model. To configure which model is being used, you can configure the variables in `whisper-config.mjs`.

### Non-English languages

To support non-English languages, you need to change the `WHISPER_MODEL` variable in `whisper-config.mjs` to a model that does not have a `.en` sufix.

## Docs

Get started with Remotion by reading the [fundamentals page](https://www.remotion.dev/docs/the-fundamentals).

## Help

We provide help on our [Discord server](https://remotion.dev/discord).

## Issues

Found an issue with Remotion? [File an issue here](https://github.com/remotion-dev/remotion/issues/new).

## License

Note that for some entities a company license is needed. [Read the terms here](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md).
