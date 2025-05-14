import React from 'react';

export default function AudioPlayer({ src }) {
  return (
    <section aria-labelledby="audio-heading">
      <h2 id="audio-heading">Explicación en voz</h2>
      <audio controls>
        <source src={src} type="audio/mp3" />
        Tu navegador no soporta audio.
      </audio>
    </section>
  );
}
