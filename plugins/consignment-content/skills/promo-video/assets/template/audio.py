"""배경 음악 + 효과음을 numpy로 직접 합성해 wav로 저장. 외부 음원 없음(상업 노출 영상이라 저작권 위험 0).

  python3 audio.py <출력.wav>

120BPM(0.5초 격자), A마이너 펜타토닉. 장면 전환·말풍선·체크·스티커 등 화면 이벤트는 timing.py를 화면과 같이 읽는다.
효과음은 음악과 같은 조(A·C·E·G) 음으로 맞추고 음악 아래에 깔리게 낮춘다.
"""
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import timing  # noqa: E402

SR = 44100
N = int(timing.END * SR)
S, R = timing.SCENES, timing.REL
BEAT = 0.5
rng = np.random.default_rng(7)

music = [np.zeros(N), np.zeros(N)]
sfx = [np.zeros(N), np.zeros(N)]


def put(bus, sig, t0, gain=1.0, pan=0.0):
    i0 = int(round(t0 * SR))
    if i0 >= N or i0 + len(sig) <= 0:
        return
    a = max(0, -i0)
    b = min(len(sig), N - i0)
    ang = (pan + 1) * np.pi / 4
    gl, gr = np.cos(ang) * gain, np.sin(ang) * gain
    bus[0][i0 + a:i0 + b] += sig[a:b] * gl
    bus[1][i0 + a:i0 + b] += sig[a:b] * gr


def tt(dur):
    return np.arange(int(dur * SR)) / SR


def decay(dur, tau, attack=0.003):
    t = tt(dur)
    e = np.exp(-t / tau)
    k = int(attack * SR)
    if k > 0:
        e[:k] *= np.linspace(0, 1, k)
    return e


def lowpass(x, w):
    w = max(1, int(w))
    cs = np.cumsum(np.concatenate([np.zeros(w), x]))
    return (cs[w:] - cs[:-w]) / w


def highpass(x, w):
    return x - lowpass(x, w)


def tone(freq, dur, tau, harm=(1.0,), detune=0.0):
    t = tt(dur)
    s = np.zeros_like(t)
    for h, a in enumerate(harm, start=1):
        s += a * np.sin(2 * np.pi * freq * h * t)
        if detune:
            s += 0.5 * a * np.sin(2 * np.pi * freq * (1 + detune) * h * t)
    return s * decay(dur, tau)


def glide(f0, f1, dur, tau, harm=(1.0,)):
    t = tt(dur)
    f = f0 * (f1 / f0) ** (t / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = sum(a * np.sin(ph * h) for h, a in enumerate(harm, start=1))
    return s * decay(dur, tau)


def kick(gain=1.0):
    d = 0.28
    t = tt(d)
    f = 48 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.11) * gain


def hat(gain=1.0, d=0.05):
    n = rng.standard_normal(int(d * SR))
    return highpass(n, 6) * decay(d, 0.012, 0.001) * gain


def clap(gain=1.0):
    d = 0.16
    n = rng.standard_normal(int(d * SR))
    n = highpass(lowpass(n, 2), 14)
    e = decay(d, 0.045, 0.001)
    # 짧은 3번 겹침으로 박수 느낌
    for off in (0.012, 0.024):
        k = int(off * SR)
        e[k:] += 0.6 * e[:-k] if k < len(e) else 0
    return n * e * gain * 0.7


def whoosh(dur=0.3, gain=1.0):
    """장면 전환용 부드러운 바람 소리. 높은 소리는 빼고 낮게 깔아 거슬리지 않게 한다."""
    n = rng.standard_normal(int(dur * SR))
    dark = lowpass(n, 110)
    mid = lowpass(n, 40)
    t = np.linspace(0, 1, len(n))
    mix = dark * (1 - t) + mid * t
    env = np.sin(np.pi * np.clip(t, 0, 1)) ** 2.4
    return mix * env * gain * 5.0


def thump(freq=70, d=0.25, gain=1.0):
    t = tt(d)
    f = freq * (1 + 1.6 * np.exp(-t / 0.03))
    ph = 2 * np.pi * np.cumsum(f) / SR
    snap = highpass(rng.standard_normal(len(t)), 10) * np.exp(-t / 0.008) * 0.25
    return (np.sin(ph) * np.exp(-t / 0.09) + snap) * gain


def pluck(freq, gain=1.0, d=0.5):
    return tone(freq, d, 0.16, harm=(1.0, 0.45, 0.2, 0.08), detune=0.003) * gain


def bass_note(freq, d, gain=1.0):
    t = tt(d)
    s = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2 * t) + 0.12 * np.sin(2 * np.pi * freq * 3 * t)
    return s * decay(d, d * 0.55, 0.008) * gain


def chime(freq, gain=1.0, d=0.7):
    return tone(freq, d, 0.28, harm=(1.0, 0.0, 0.25, 0.0, 0.1)) * gain


# ---- 음 높이 (A마이너 펜타토닉 + 코드)
CHORDS = [  # (베이스, 코드 3음)
    (110.00, (440.00, 523.25, 659.25)),   # Am
    (87.31, (349.23, 440.00, 523.25)),    # F
    (130.81, (523.25, 659.25, 783.99)),   # C
    (98.00, (392.00, 493.88, 587.33)),    # G
]
E5, G5, A5, C6, D6, E6, G6 = 659.25, 783.99, 880.00, 1046.50, 1174.66, 1318.51, 1567.98


def in_range(t, a, b):
    return a <= t < b - 1e-9


# ---- 음악 ----
BAR = 4 * BEAT
n_bars = int(timing.END / BAR)
TENSION = (S["C"], S["D1"])
FULL = (S["D1"], S["F"])
LIGHT = (0.0, S["C"])

for bar in range(n_bars):
    t0 = bar * BAR
    root, tones = CHORDS[bar % 4]
    mid = t0 + BAR / 2
    tension = in_range(t0, *TENSION)
    full = in_range(t0, *FULL) or in_range(t0, S["F"], timing.END)
    light = in_range(t0, *LIGHT)
    if t0 >= S["F"]:
        continue  # 마무리는 아래에서 따로
    # 베이스: 8분음표, 긴장 구간은 낮은 한 음 지속
    if tension:
        put(music, bass_note(55.0, BAR, 0.55), t0, 1.0)
    else:
        for k in range(8):
            f = root if k % 4 != 3 else root * 1.5
            put(music, bass_note(f, 0.24, 0.5 if full else 0.42), t0 + k * 0.25, 1.0)
    # 킥
    for b in range(4):
        tb = t0 + b * BEAT
        if tension:
            if b == 0:
                put(music, kick(0.55), tb, 1.0)
        else:
            put(music, kick(0.85 if full else 0.65), tb, 1.0)
    # 하이햇
    for k in range(8):
        tk = t0 + k * 0.25
        if tension:
            put(music, hat(0.14), tk, 1.0, pan=0.25)
        elif k % 2 == 1:
            put(music, hat(0.30 if full else 0.22), tk, 1.0, pan=0.25)
    # 박수 (2·4박)
    if (full or t0 >= S["B"]) and not tension:
        for b in (1, 3):
            put(music, clap(0.55 if full else 0.32), t0 + b * BEAT, 1.0)
    # 플럭 아르페지오
    if not tension:
        pat = [0, 1, 2, 1, 0, 1, 2, 2]
        for k in range(8):
            put(music, pluck(tones[pat[k]], 0.20 if full else 0.15), t0 + k * 0.25, 1.0, pan=-0.2 + 0.1 * (k % 3))
        if full:
            put(music, pluck(tones[0] * 2, 0.07, 0.35), t0 + 0.0, 1.0, pan=0.3)

# E 장면: 반짝이는 멜로디 얹기
mel = [E5, G5, A5, G5, C6, A5, G5, E5]
for k, f in enumerate(mel * 2):
    t = S["E"] + k * 0.25
    if t < S["F"]:
        put(music, chime(f, 0.14, 0.4), t, 1.0, pan=0.35)

# A 시작: 코드 스탭 (훅)
for f in (220.0, 329.63, 440.0, 523.25, 659.25):
    put(music, tone(f, 0.9, 0.35, harm=(1.0, 0.4, 0.15)), 0.0, 0.12)
put(music, kick(1.0), 0.0, 1.0)

# C → D1 직전 라이저와 D1 임팩트
rise_t0 = S["D1"] - 1.4
n = rng.standard_normal(int(1.4 * SR))
rise = highpass(n, 8) * np.linspace(0, 1, len(n)) ** 2.2
put(music, rise, rise_t0, 0.10)
put(music, thump(55, 0.6, 1.1), S["D1"], 1.0)
put(music, hat(0.8, 0.35), S["D1"], 0.6)

# ---- F 마무리: C메이저 스탭 + 크래시 + 잔향
fa = S["F"]
for f in (130.81, 261.63, 329.63, 392.00, 523.25, 659.25, 783.99):
    put(music, tone(f, 2.3, 1.0, harm=(1.0, 0.4, 0.15)), fa, 0.11)
put(music, kick(1.0), fa, 1.0)
put(music, thump(50, 0.8, 1.0), fa, 0.9)
crash = highpass(rng.standard_normal(int(1.6 * SR)), 5) * decay(1.6, 0.45, 0.002)
put(music, crash, fa, 0.28)
for b in range(1, 5):
    put(music, kick(0.55), fa + b * BEAT, 1.0)
    put(music, hat(0.25), fa + b * BEAT + 0.25, 1.0, pan=0.25)

# ---- 효과음 ----
def pops(times, freqs, gain=0.22, pan_alt=True):
    for i, (t, f) in enumerate(zip(times, freqs)):
        sig = glide(f * 0.6, f, 0.14, 0.05, harm=(1.0, 0.25))
        put(sfx, sig, t, gain, pan=(-0.25 if i % 2 == 0 else 0.25) if pan_alt else 0)


# 장면 전환 — 아래에서 올라오는 닦아내기 + 낮은 한 방
for k in ("B", "C", "D1", "D2", "D3", "E"):
    put(sfx, whoosh(0.3, 0.10), S[k] - 0.08, 1.0)
    put(sfx, thump(75, 0.22, 0.28), S[k] + 0.12, 1.0)
put(sfx, whoosh(0.3, 0.10), S["F"] - 0.08, 1.0)

# A
a = S["A"]
put(sfx, thump(80, 0.2, 0.55), a + R["A"]["l1"] + 0.1, 1.0)
put(sfx, thump(80, 0.2, 0.55), a + R["A"]["l2"] + 0.1, 1.0)
for t, f in zip(R["A"]["spec"], (220.0, 261.63, 329.63)):
    put(sfx, tone(f, 0.18, 0.06, harm=(1.0, 0.5)), a + t + 0.05, 0.28)
    put(sfx, thump(110, 0.12, 0.3), a + t + 0.05, 1.0)

# B — 체크 표시
for t, f in zip(R["B"]["items"], (A5, C6, E6, G6)):
    put(sfx, tone(f, 0.16, 0.05, harm=(1.0, 0.3)), S["B"] + t + 0.14, 0.26, pan=0.2)
put(sfx, chime(A5, 0.18, 0.8), S["B"] + R["B"]["verdict"], 1.0)

# C — 말풍선, 숫자 올라가기, 반전
pops([S["C"] + x for x in R["C"]["bubbles"]], (E5, G5, A5, C6), 0.24)
c0, c1 = R["C"]["count"]
steps = 9
for i in range(steps):
    f = A5 * (1.0 + 0.05 * i)
    put(sfx, tone(f, 0.05, 0.02, harm=(1.0, 0.3)), S["C"] + c0 + (c1 - c0) * i / (steps - 1), 0.20)
put(sfx, thump(60, 0.5, 0.9), S["C"] + c1, 1.0)
put(sfx, chime(E5, 0.14, 0.6), S["C"] + R["C"]["cap"], 1.0)
put(sfx, thump(70, 0.3, 0.6), S["C"] + R["C"]["turn"], 1.0)
put(sfx, chime(A5, 0.16, 0.9), S["C"] + R["C"]["turn"] + 0.3, 1.0)

# D1
d1 = S["D1"]
put(sfx, glide(450, 900, 0.3, 0.1, harm=(1.0, 0.2)), d1 + R["D1"]["ellipse"], 0.16)
put(sfx, chime(E6, 0.22, 0.5), d1 + R["D1"]["ok"] + 0.05, 1.0, pan=0.2)
put(sfx, tone(220.0, 0.22, 0.09, harm=(1.0, 0.7, 0.4)), d1 + R["D1"]["no"] + 0.05, 0.22, pan=-0.2)

# D2 — 스티커 쾅
d2 = S["D2"] + R["D2"]["sticker"]
put(sfx, thump(65, 0.35, 1.0), d2 + 0.12, 1.0)
put(sfx, tone(196.0, 0.18, 0.05, harm=(1.0, 0.8, 0.5)), d2 + 0.12, 0.25)

# D3 — 막대 3줄이 그려지는 소리, 공식
for i, t in enumerate(R["D3"]["bars"]):
    put(sfx, glide(260 * (1 + 0.12 * i), 520 * (1 + 0.12 * i), 0.3, 0.12, harm=(1.0, 0.25)), S["D3"] + t, 0.18, pan=(-0.3, 0.3, 0.0)[i])
    put(sfx, tone((C6, E6, G6)[i], 0.22, 0.08, harm=(1.0, 0.3)), S["D3"] + t + 0.25, 0.20)
put(sfx, thump(70, 0.3, 0.7), S["D3"] + R["D3"]["formula"] + 0.15, 1.0)

# E — 꾹! 꾹!
for t in R["E"]["steps"]:
    put(sfx, thump(120, 0.16, 0.9), S["E"] + t + 0.3, 1.0)
    put(sfx, tone(A5, 0.12, 0.04, harm=(1.0, 0.3)), S["E"] + t + 0.3, 0.14)

# F
f0 = S["F"]
put(sfx, thump(80, 0.2, 0.6), f0 + R["F"]["h1"] + 0.1, 1.0)
put(sfx, thump(80, 0.2, 0.6), f0 + R["F"]["h1"] + 0.3, 1.0)
put(sfx, thump(100, 0.2, 0.5), f0 + R["F"]["spec"] + 0.1, 1.0)
pops([f0 + x for x in R["F"]["labels"]], (G5, A5, C6), 0.24, pan_alt=False)

# ---- 믹스 ----
def reverb(bus, mix=0.14, rt=0.55):
    n = int(rt * SR)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / (rt * SR / 4.5))
    ir[0] = 0
    out = []
    for ch in bus:
        wet = np.fft.irfft(np.fft.rfft(ch, N + n) * np.fft.rfft(ir, N + n), N + n)[:N]
        out.append(ch + mix * wet / (np.max(np.abs(wet)) + 1e-9) * np.max(np.abs(ch)))
    return out


MUSIC_GAIN, SFX_GAIN = 0.55, 0.70
musicr = reverb(music, 0.10)
sfxr = reverb(sfx, 0.22, 0.4)
mix = [MUSIC_GAIN * m + SFX_GAIN * s for m, s in zip(musicr, sfxr)]
peak = max(np.max(np.abs(mix[0])), np.max(np.abs(mix[1])))
mix = [np.tanh(1.3 * ch / peak) / np.tanh(1.3) * 0.9 for ch in mix]

# 끝 0.5초 페이드아웃
fade = int(0.5 * SR)
for ch in mix:
    ch[-fade:] *= np.linspace(1, 0, fade)

out = Path(sys.argv[1])
pcm = (np.stack(mix, axis=1) * 32767).astype("<i2")
with wave.open(str(out), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote", out, f"{N / SR:.1f}s", "peak", float(np.max(np.abs(pcm)) / 32767))
