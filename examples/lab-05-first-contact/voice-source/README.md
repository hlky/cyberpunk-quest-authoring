# Lab 5 voice-source provenance

`contact_i_85c3283507e7ef2f.wav` is the canonical, mod-owned source recording
for the line `All clear. Keep moving.` Its locstring RUID is
`9638591835734011695`; the lowercase hexadecimal representation of that ID is
the filename suffix `85c3283507e7ef2f`.

The source was synthesized with eSpeak NG 1.50 (`en-us+f3`, speed 145, pitch
42, amplitude 160), then normalized with ffmpeg to 48 kHz, mono, signed 16-bit
PCM with `loudnorm`. The WAV is 249,160 bytes, approximately 2.594604 seconds,
and has SHA-256
`ca63bdebd64a1312f53a4fe04f381b97cd9b3e11c04c19b815a503b0b5a11110`.

The checked WEM was produced from that WAV with WwiseConsole 2025.1.7.9143,
`convert-external-source`, Windows platform, `Vorbis Quality High`. It is
21,379 bytes, 48 kHz mono, approximately 2.598188 seconds, and has SHA-256
`0487ba1116d9c4fa9cfb25e825ad4ec35110195cf3953cb8bc67a16f5cbc657f`.

Wwise conversion is not claimed to be byte reproducible across machines,
versions, installations, or codec plug-ins. The hash-pinned WEM in each
checkpoint is the executable reference asset. WEM production is taught later,
not made a Lab 5 reader prerequisite.

The WAV and WEM are original Lab 5 assets licensed under the repository's CC
BY 4.0 example license. No eSpeak NG executable/voice data or Wwise project is
redistributed.

SPDX-License-Identifier: CC-BY-4.0
