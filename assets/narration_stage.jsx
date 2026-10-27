/**
 * narration_stage.jsx · narration-driven Stage
 *
 * ╔════════════════════════════════════════════════════════════════════════════╗
 * ║  🛑 Must read before using this toolkit: references/voiceover-pipeline.md  ║
 * ║                                                                            ║
 * ║  Iron rule #1: the whole film is one continuous motion narrative,          ║
 * ║          not a set of separate scenes                                      ║
 * ║          You are not making 7 slides. You are directing 1 movie.           ║
 * ║                                                                            ║
 * ║  Iron rule #2: the chosen hero element persists across scenes;             ║
 * ║          don't make a new layout for every segment                         ║
 * ║                                                                            ║
 * ║  Iron rule #3: no hard cuts between scenes (opacity 1→0/0→1)               ║
 * ║          Morph, don't cut                                                  ║
 * ║                                                                            ║
 * ║  Failure mode #1 (a real pitfall hit in this skill's v1):                  ║
 * ║          each Scene has its own independent layout + cues use fade-up      ║
 * ║          + scene changes are whole-page opacity switches                   ║
 * ║          = PowerPoint with a voiceover = all texture gone                 ║
 * ║                                                                            ║
 * ║  Correct approach: put the hero directly as a child of <NarrationStage>    ║
 * ║          (not inside a Scene)                                              ║
 * ║          use useNarration() inside the hero to read time/scene/cue state   ║
 * ║          the hero decides its own form from the current time               ║
 * ║          → continuous motion across scenes                                 ║
 * ╚════════════════════════════════════════════════════════════════════════════╝
 *
 * Usage (inline in the HTML's <script type="text/babel">):
 *   const { NarrationStage, Scene, Cue, useNarration } = NarrationStageLib;
 *
 *   const App = () => (
 *     <NarrationStage timeline={TIMELINE} audioSrc="voiceover.mp3"
 *                     width={1920} height={1080}>
 *       <Scene id="intro">
 *         <h1>What is a token</h1>
 *         <Cue id="question">
 *           {(triggered) => triggered && <p>↑ This is the question</p>}
 *         </Cue>
 *       </Scene>
 *       <Scene id="token-2">
 *         <Cue id="split">
 *           {(triggered, progress) => (
 *             <div style={{opacity: triggered ? 1 : 0.3}}>...</div>
 *           )}
 *         </Cue>
 *       </Scene>
 *     </NarrationStage>
 *   );
 *
 * Time source (chosen automatically, one of two):
 *   - Video recording mode (window.__recording === true): uses window.__time (an external driver pushes frames)
 *   - Live playback mode: uses the <audio> element's currentTime (strictly synced with the audio when the user presses play)
 *
 * Compatible with render-video.js:
 *   - sets window.__ready = true on the first tick frame
 *   - when recording video, detects window.__recording, forces audio not to play, and uses window.__time
 *   - exposes window.__totalDuration so the driver can compute the total frame count
 *
 * Dependencies: React 18 + ReactDOM 18 + Babel standalone (same as animations.jsx)
 */

const NarrationStageLib = (() => {
  const NarrationContext = React.createContext({
    time: 0,
    scene: null,
    sceneTime: 0,
    isCueTriggered: () => false,
    cueProgress: () => 0,
  });

  /**
   * Main component: takes timeline + audio, provides context
   *
   * Props:
   *   timeline       timeline.json object (required)
   *   audioSrc       voiceover.mp3 path (required)
   *   width/height   Stage size, default 1920x1080
   *   background     default '#0e0e0e'
   *   controls       whether to show the bottom playback bar, default true
   *   children       animation content (organized with <Scene>/<Cue>)
   */
  function NarrationStage({
    timeline,
    audioSrc,
    width = 1920,
    height = 1080,
    background = '#0e0e0e',
    controls = true,
    children,
  }) {
    const audioRef = React.useRef(null);
    const [time, setTime] = React.useState(0);
    const [playing, setPlaying] = React.useState(false);
    const recording = typeof window !== 'undefined' && window.__recording === true;

    // Exposed to render-video.js
    React.useEffect(() => {
      if (typeof window === 'undefined') return;
      window.__totalDuration = timeline.totalDuration;
      window.__ready = true;
    }, [timeline.totalDuration]);

    // Time tick
    React.useEffect(() => {
      let raf;
      if (recording) {
        // Seek-render (render-video-seek.js injects window.__seekRender): freeze the self-driven clock,
        // advance frame by frame via the external window.__seek(t). Every frame is a deterministic seek; no rAF is started.
        if (typeof window !== 'undefined' && window.__seekRender) {
          window.__seek = (t) => setTime(Math.min(t, timeline.totalDuration));
          return;
        }
        // Video recording mode: rAF wall-clock self-drives, starting from 0
        // Compatible with render-video.js (it relies on the animation advancing naturally + window.__seek to reset)
        let startedAt = null;
        const tick = (now) => {
          if (startedAt === null) startedAt = now;
          setTime(Math.min((now - startedAt) / 1000, timeline.totalDuration));
          raf = requestAnimationFrame(tick);
        };
        raf = requestAnimationFrame(tick);
        // Expose __seek so render-video.js can call __seek(0) after ready to reset
        if (typeof window !== 'undefined') {
          window.__seek = (t) => {
            startedAt = performance.now() - t * 1000;
            setTime(t);
          };
        }
      } else {
        // Live playback mode: follow audio.currentTime
        const tick = () => {
          if (audioRef.current && !audioRef.current.paused) {
            setTime(audioRef.current.currentTime);
          }
          raf = requestAnimationFrame(tick);
        };
        tick();
      }
      return () => cancelAnimationFrame(raf);
    }, [recording, timeline.totalDuration]);

    // Current scene
    const currentScene = React.useMemo(() => {
      if (!timeline.scenes) return null;
      // Find the segment where start <= time < end. The last segment holds until end
      for (let i = 0; i < timeline.scenes.length; i++) {
        const s = timeline.scenes[i];
        const next = timeline.scenes[i + 1];
        if (time >= s.start && (!next || time < next.start)) return s;
      }
      return timeline.scenes[0];
    }, [time, timeline.scenes]);

    const sceneTime = currentScene ? Math.max(0, time - currentScene.start) : 0;

    // Find cue state (compared by absoluteTime, so it works across scenes too)
    const allCues = React.useMemo(() => {
      const map = {};
      for (const s of timeline.scenes || []) {
        for (const c of s.cues || []) {
          map[c.id] = c;
        }
      }
      return map;
    }, [timeline.scenes]);

    const isCueTriggered = React.useCallback(
      (cueId) => {
        const c = allCues[cueId];
        if (!c) return false;
        return time >= c.absoluteTime;
      },
      [allCues, time],
    );

    /** Seconds after triggering, 0→1; stays at 1 after >1. Used for fade-in animations after a cue */
    const cueProgress = React.useCallback(
      (cueId, ramp = 0.5) => {
        const c = allCues[cueId];
        if (!c) return 0;
        const dt = time - c.absoluteTime;
        if (dt <= 0) return 0;
        if (dt >= ramp) return 1;
        return dt / ramp;
      },
      [allCues, time],
    );

    const ctx = { time, scene: currentScene, sceneTime, isCueTriggered, cueProgress, timeline };

    // play/pause/seek controls
    const handlePlayPause = () => {
      if (!audioRef.current) return;
      if (audioRef.current.paused) {
        audioRef.current.play();
        setPlaying(true);
      } else {
        audioRef.current.pause();
        setPlaying(false);
      }
    };

    const handleSeek = (e) => {
      if (!audioRef.current) return;
      const t = parseFloat(e.target.value);
      audioRef.current.currentTime = t;
      setTime(t);
    };

    const handleAudioEnded = () => setPlaying(false);

    return (
      <NarrationContext.Provider value={ctx}>
        <div
          style={{
            position: 'relative',
            width,
            height,
            background,
            overflow: 'hidden',
            color: '#fff',
            fontFamily: '-apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif',
          }}
        >
          {children}
        </div>
        {!recording && (
          <audio
            ref={audioRef}
            src={audioSrc}
            preload="auto"
            onEnded={handleAudioEnded}
          />
        )}
        {!recording && controls && (
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 12,
              padding: '12px 16px',
              background: '#1a1a1a',
              color: '#ddd',
              fontFamily: 'monospace',
              fontSize: 13,
              width,
              boxSizing: 'border-box',
            }}
          >
            <button
              onClick={handlePlayPause}
              style={{
                padding: '6px 14px',
                background: '#fff',
                color: '#000',
                border: 0,
                borderRadius: 4,
                cursor: 'pointer',
                fontWeight: 600,
              }}
            >
              {playing ? '❚❚ Pause' : '▶ Play'}
            </button>
            <input
              type="range"
              min={0}
              max={timeline.totalDuration}
              step={0.01}
              value={time}
              onChange={handleSeek}
              style={{ flex: 1 }}
            />
            <span style={{ minWidth: 110, textAlign: 'right' }}>
              {time.toFixed(2)} / {timeline.totalDuration.toFixed(2)}s
            </span>
            <span
              style={{
                padding: '4px 10px',
                background: '#2a2a2a',
                borderRadius: 4,
                minWidth: 100,
                textAlign: 'center',
              }}
            >
              {currentScene ? currentScene.id : '—'}
            </span>
          </div>
        )}
      </NarrationContext.Provider>
    );
  }

  /**
   * Scene wrapper: renders children only while the given scene id is active
   *
   * Props:
   *   id        scene id (matches timeline.scenes[].id)
   *   children  content to render; can be a ReactNode or (sceneTime, sceneInfo) => ReactNode
   *   keepMounted default false. If true, stays mounted and only toggles visibility (use when animation continuity needs it)
   */
  function Scene({ id, children, keepMounted = false }) {
    const { scene, sceneTime } = React.useContext(NarrationContext);
    const isActive = scene && scene.id === id;
    if (!isActive && !keepMounted) return null;
    const content = typeof children === 'function' ? children(sceneTime, scene) : children;
    return (
      <div
        style={{
          position: 'absolute',
          inset: 0,
          opacity: isActive ? 1 : 0,
          pointerEvents: isActive ? 'auto' : 'none',
          transition: keepMounted ? 'opacity 0.2s' : undefined,
        }}
      >
        {content}
      </div>
    );
  }

  /**
   * Cue wrapper: listens for the cue's trigger state
   *
   * Props:
   *   id        cue id (matches timeline.scenes[].cues[].id)
   *   ramp      ramp duration (seconds) for progress 0→1 after the cue triggers, default 0.5
   *   children  must be a function: (triggered: bool, progress: 0-1) => ReactNode
   */
  function Cue({ id, ramp = 0.5, children }) {
    const { isCueTriggered, cueProgress } = React.useContext(NarrationContext);
    const triggered = isCueTriggered(id);
    const progress = cueProgress(id, ramp);
    return children(triggered, progress);
  }

  /** Hook: get the narration state directly in a custom component */
  function useNarration() {
    return React.useContext(NarrationContext);
  }

  /**
   * splitChunkToLines · splits a piece of text at punctuation into short lines of ≤maxLen characters
   *
   * Used for subtitle display: the Bilibili standard is ≤12 characters per line for readability. This function:
   * 1. First splits into sentences at strong punctuation (。！？\n), never cutting across a full stop
   * 2. A sentence ≤ maxLen is used as is; otherwise it is sliced at weak punctuation (，、；：) and merged
   * 3. Mixed Chinese and English: English letters/digits count as 0.5 character of visual width
   * 4. Hard-cut fallback (rare: a single punctuation segment exceeds maxLen)
   * dstack: mostly-Latin text (English) takes a separate path: sentences end at . ! ? (followed by a space),
   *   clauses at , ; :, lines wrap only at word boundaries, and maxLen is in characters (default 42).
   *   CJK and CJK-dominant mixed text keep the original behaviour exactly.
   *
   * @param text   source text
   * @param maxLen max visual length per line; default 13 for CJK (≈12 characters + one punctuation mark), 42 characters for English
   * @returns array of split subtitle lines
   */
  function visualLen(s) {
    let n = 0;
    for (const ch of s) n += /[a-zA-Z0-9 .,'":;\-]/.test(ch) ? 0.5 : 1;
    return n;
  }
  const CJK_RE = /[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af\u3000-\u303f\uff00-\uffef]/;
  const EN_MAX = 42;
  function isLatinText(s) {
    let cjk = 0, latin = 0;
    for (const ch of s) { if (CJK_RE.test(ch)) cjk++; else if (/[A-Za-z]/.test(ch)) latin++; }
    return latin > 0 && cjk * 2 < latin * 0.2;  // CJK chars carry ~2x the content of a Latin letter
  }
  function needsSpace(prev, cur) {
    if (!prev || !cur) return false;
    const a = prev[prev.length - 1], b = cur[0];
    if (/\s/.test(a) || /\s/.test(b)) return false;
    if (CJK_RE.test(a) || CJK_RE.test(b)) return false;
    if (/[,.;:!?%)\]}'"”’…]/.test(b) || /[(\[{“‘]/.test(a)) return false;
    return true;
  }
  function joinTokens(tokens) {
    let out = '';
    for (const t of tokens) out += (needsSpace(out, t) ? ' ' : '') + t;
    return out;
  }
  function wrapWords(text, max) {
    const out = [];
    let cur = '';
    for (const w of text.split(/\s+/).filter(Boolean)) {
      if (cur && cur.length + 1 + w.length > max) { out.push(cur); cur = w; }
      else cur = cur ? cur + ' ' + w : w;
    }
    if (cur) out.push(cur);
    return out;
  }
  function splitLatinToLines(text, max) {
    const lines = [];
    const sentences = text.split(/\n+|(?<=[.!?…]["')\]”’]*)\s+/).map(x => x.trim()).filter(Boolean);
    for (const sent of sentences) {
      if (sent.length <= max) { lines.push(sent); continue; }
      const parts = sent.split(/(?<=[,;:])\s+/).filter(Boolean);
      let merged = '';
      for (const p of parts) {
        if (!merged) merged = p;
        else if (merged.length + 1 + p.length <= max) merged += ' ' + p;
        else { lines.push(...wrapWords(merged, max)); merged = p; }
      }
      if (merged) lines.push(...wrapWords(merged, max));
    }
    return lines;
  }
  function splitChunkToLines(text, maxLen = null) {
    if (isLatinText(text)) return splitLatinToLines(text, maxLen || EN_MAX);
    if (maxLen == null) maxLen = 13;
    const lines = [];
    const sentences = [];
    let buf = '';
    for (const ch of text) {
      buf += ch;
      if ('。！？\n'.includes(ch)) { if (buf.trim()) sentences.push(buf.trim()); buf = ''; }
    }
    if (buf.trim()) sentences.push(buf.trim());
    for (const sent of sentences) {
      if (visualLen(sent) <= maxLen) { lines.push(sent); continue; }
      const parts = [];
      let pbuf = '';
      for (const ch of sent) {
        pbuf += ch;
        if ('，、；：'.includes(ch)) { parts.push(pbuf); pbuf = ''; }
      }
      if (pbuf) parts.push(pbuf);
      let merged = '';
      for (const p of parts) {
        if (visualLen(merged) + visualLen(p) <= maxLen) merged += p;
        else { if (merged) lines.push(merged); merged = p; }
      }
      if (merged) {
        if (visualLen(merged) <= maxLen) lines.push(merged);
        else {
          let hbuf = '';
          for (const ch of merged) { hbuf += ch; if (visualLen(hbuf) >= maxLen) { lines.push(hbuf); hbuf = ''; } }
          if (hbuf) lines.push(hbuf);
        }
      }
    }
    return lines.filter(l => l.trim());
  }

  /**
   * Subtitles · Bilibili-style subtitle component (dark ink text with a white halo, no background, shown by chunk timing)
   *
   * Automatically takes the active chunk from the current scene.chunks, splits it into short lines with splitChunkToLines,
   * and allocates the chunk's time window to each line in proportion to character count.
   *
   * Required: timeline.scenes[].chunks[] (narrate-pipeline.mjs outputs this by default)
   *
   * Props (override the default styles):
   *   bottom    pixels from the bottom, default 90 (not flush with the edge)
   *   fontSize  font size, default 32
   *   color     text color, default dark ink #1a1a1a (suits a light paper-white background)
   *   haloColor halo color, default rgba(245,241,232,0.9) (suits a #f5f1e8 background)
   *   maxLen    max line length; default 13 visual units for CJK, 42 characters for English
   *
   * Dark-background scenes: just change color to '#fff' and haloColor to 'rgba(0,0,0,0.85)'.
   *
   * Karaoke mode (character-level highlight; needs words in the timeline chunks, which narrate-pipeline.mjs outputs by default):
   *   karaoke       true to enable, default false. Shows the whole line; each character changes color as it is read
   *   karaokeColor  color of characters already read, default brand orange '#e8590c'
   *   When a chunk has no words data, it automatically falls back to normal chunk mode; the caller doesn't need to check.
   *   Note: a TTS may return words as normalized text (e.g. "2025" may come back as
   *   "twenty twenty-five"); karaoke lines are built directly from words,
   *   which keeps highlighting strictly aligned with pronunciation (may differ from the original chunk.text).
   */
  function splitWordsToLines(words, maxLen = null) {
    // Greedily pack character-level timestamp tokens into lines of ≤maxLen; force a line break after strong punctuation (。！？), never crossing a full stop
    if (isLatinText(joinTokens(words.map(w => w.text)))) {
      // dstack English path: word tokens, line length in characters incl. spaces, break after . ! ?
      const max = maxLen || EN_MAX;
      const out = [];
      let line = [];
      for (const w of words) {
        if (line.length > 0 && joinTokens(line.map(x => x.text).concat(w.text)).length > max) { out.push(line); line = []; }
        line.push(w);
        if (/[.!?…。！？]["')\]”’]*\s*$/.test(w.text)) { out.push(line); line = []; }
      }
      if (line.length > 0) out.push(line);
      return out;
    }
    if (maxLen == null) maxLen = 13;
    const lines = [];
    let cur = [];
    let curLen = 0;
    for (const w of words) {
      const wLen = visualLen(w.text);
      if (cur.length > 0 && curLen + wLen > maxLen) { lines.push(cur); cur = []; curLen = 0; }
      cur.push(w);
      curLen += wLen;
      if (/[。！？]\s*$/.test(w.text)) { lines.push(cur); cur = []; curLen = 0; }
    }
    if (cur.length > 0) lines.push(cur);
    return lines;
  }

  function Subtitles({ bottom = 90, fontSize = 32, color = '#1a1a1a', haloColor = 'rgba(245,241,232,0.9)', maxLen = null, karaoke = false, karaokeColor = '#e8590c' } = {}) {
    const { time, scene } = React.useContext(NarrationContext);
    if (!scene || !scene.chunks) return null;
    const active = scene.chunks.find(c => time >= c.absoluteStart && time < c.absoluteEnd);
    if (!active) return null;

    // -- Karaoke mode: whole line shown + per-character highlight (changes color as soon as it's read, no CSS transition, deterministic for seek rendering) --
    if (karaoke && active.words && active.words.length > 0) {
      const wordLines = splitWordsToLines(active.words, maxLen);
      let activeWLine = wordLines[0];
      for (const ln of wordLines) {
        if (time >= ln[0].absoluteStart) activeWLine = ln;
        else break;
      }
      const lineStart = activeWLine[0].absoluteStart;
      const lineProg = Math.max(0, Math.min(1, (time - (lineStart - 0.15)) / 0.15)); // line fades in 0.15s early
      return React.createElement('div', {
        style: { position: 'absolute', left: 0, right: 0, bottom, display: 'flex', justifyContent: 'center', pointerEvents: 'none', zIndex: 50 },
      }, React.createElement('div', {
        key: lineStart,
        style: {
          fontFamily: '"PingFang SC", "Noto Sans SC", -apple-system, sans-serif',
          fontSize, fontWeight: 600,
          letterSpacing: '0.04em', lineHeight: 1.2, textAlign: 'center',
          textShadow: `0 0 6px ${haloColor}, 0 0 12px ${haloColor}, 0 1px 2px rgba(255,255,255,0.5)`,
          opacity: lineProg, transform: `translateY(${(1 - lineProg) * 4}px)`,
        },
      }, activeWLine.map((w, i) => React.createElement('span', {
        key: i,
        style: { color: time >= w.absoluteStart ? karaokeColor : color },
      }, (i > 0 && needsSpace(activeWLine[i - 1].text, w.text) ? ' ' : '') + w.text))));
    }

    // -- Normal chunk mode (original behavior, unchanged) --
    const lines = splitChunkToLines(active.text, maxLen);
    if (lines.length === 0) return null;
    const totalLen = lines.reduce((s, l) => s + visualLen(l), 0);
    const chunkDur = active.absoluteEnd - active.absoluteStart;
    let acc = active.absoluteStart;
    let activeLine = lines[lines.length - 1];
    let lineStart = active.absoluteStart;
    for (const line of lines) {
      const dur = (visualLen(line) / totalLen) * chunkDur;
      if (time < acc + dur) { activeLine = line; lineStart = acc; break; }
      acc += dur;
    }
    const lineProg = Math.min(1, (time - lineStart) / 0.15);
    return React.createElement('div', {
      style: { position: 'absolute', left: 0, right: 0, bottom, display: 'flex', justifyContent: 'center', pointerEvents: 'none', zIndex: 50 },
    }, React.createElement('div', {
      key: lineStart,
      style: {
        fontFamily: '"PingFang SC", "Noto Sans SC", -apple-system, sans-serif',
        fontSize, fontWeight: 600, color,
        letterSpacing: '0.04em', lineHeight: 1.2, textAlign: 'center',
        textShadow: `0 0 6px ${haloColor}, 0 0 12px ${haloColor}, 0 1px 2px rgba(255,255,255,0.5)`,
        opacity: lineProg, transform: `translateY(${(1 - lineProg) * 4}px)`,
      },
    }, activeLine));
  }

  /**
   * useSceneFade · soft fade-in/fade-out helper for supporting elements inside a scene
   *
   * Iron rule #2 forbids hard cuts between scenes, but supporting elements inside a scene (data cards, quote blocks)
   * stay lit by default until the scene ends once their cue triggers. If they don't fade out, then when leaving this segment for the next one
   * these elements linger awkwardly or vanish instantly. This hook provides a unified soft transition of [entry fade-in → hold → exit fade-out].
   *
   * Usage (multiply op into the supporting element's opacity):
   *   const op = useSceneFade('md-side', 0.6, 0.8);  // in 0.6s, out 0.8s
   *   <Cue id="agents-md">{(t, p) => (
   *     <div style={{ opacity: op * p }}>...</div>
   *   )}</Cue>
   *
   * This way the data card fades in within 0.6s of the md-side segment starting, starts fading out 0.8s before the segment ends,
   * and overlaps with the next segment's supporting elements fading in, so the frame never hard-cuts.
   *
   * @param sceneId  scene id
   * @param fadeIn   entry fade-in seconds (default 0.5)
   * @param fadeOut  exit fade-out seconds (default 0.5)
   * @returns opacity multiplier between 0 and 1
   */
  function useSceneFade(sceneId, fadeIn = 0.5, fadeOut = 0.5) {
    const { time, timeline } = React.useContext(NarrationContext);
    if (!timeline) return 0;
    const s = timeline.scenes.find(x => x.id === sceneId);
    if (!s) return 0;
    const inT = (time - s.start) / fadeIn;
    const outT = (s.end - time) / fadeOut;
    const v = Math.min(1, Math.min(inT, outT));
    return Math.max(0, v);
  }

  return { NarrationStage, Scene, Cue, useNarration, useSceneFade, Subtitles, splitChunkToLines, splitWordsToLines, joinTokens };
})();

if (typeof window !== 'undefined') {
  Object.assign(window, { NarrationStageLib });
}
