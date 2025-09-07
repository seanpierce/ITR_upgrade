export class LiveService {
  private audio: HTMLAudioElement | null = null;

  constructor(private initialVolume: number = 0.8) {}

  setAudio(url: string, volume: number, onLoaded?: () => void, onError?: () => void) {
    this.audio?.pause();
    const audio = new Audio();
    audio.src = url;
    audio.volume = volume;
    audio.preload = 'metadata';

    audio.addEventListener('loadeddata', () => {
      if (audio.readyState >= 2 && onLoaded) {
        onLoaded();
      }
    });

    audio.addEventListener('error', () => {
      console.error('Audio error', new Date());
      if (onError) onError();
    });

    this.audio = audio;
    return audio;
  }

  play() {
    this.audio?.play();
  }

  stop() {
    this.audio?.pause();
  }

  setVolume(volume: number) {
    if (this.audio) this.audio.volume = volume;
  }

  getAudio() {
    return this.audio;
  }
}
