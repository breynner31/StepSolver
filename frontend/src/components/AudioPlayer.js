import React, { useEffect, useRef, useState } from 'react';

export default function AudioPlayer({ src }) {
  const audioRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    const audio = audioRef.current;
    
    // Configurar el audio para reproducir automáticamente
    audio.load();
    audio.play().catch(error => {
      console.log("Reproducción automática no permitida:", error);
    });

    // Eventos del audio
    const handleTimeUpdate = () => setCurrentTime(audio.currentTime);
    const handleLoadedMetadata = () => setDuration(audio.duration);
    const handleEnded = () => setIsPlaying(false);

    audio.addEventListener('timeupdate', handleTimeUpdate);
    audio.addEventListener('loadedmetadata', handleLoadedMetadata);
    audio.addEventListener('ended', handleEnded);

    return () => {
      audio.removeEventListener('timeupdate', handleTimeUpdate);
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
      audio.removeEventListener('ended', handleEnded);
    };
  }, [src]);

  const togglePlayPause = () => {
    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  const formatTime = (time) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <section aria-labelledby="audio-heading" className="audio-section">
      <h2 id="audio-heading">Explicación en voz</h2>
      <div className="audio-player">
        <audio ref={audioRef} src={src} />
        
        <div className="audio-controls">
          <button 
            onClick={togglePlayPause}
            className="play-pause-btn"
            aria-label={isPlaying ? "Pausar" : "Reproducir"}
          >
            {isPlaying ? "⏸️" : "▶️"}
          </button>
          
          <div className="progress-container">

            <input
              type="range"
              min="0"
              max={duration}
              value={currentTime}
              onChange={(e) => {
                audioRef.current.currentTime = e.target.value;
                setCurrentTime(e.target.value);
              }}
              className="progress-slider"
            />
          </div>
          
          <div className="time-display">
            {formatTime(currentTime)} / {formatTime(duration)}
          </div>
        </div>
      </div>
    </section>
  );
}