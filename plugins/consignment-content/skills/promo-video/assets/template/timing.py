"""영상 타이밍 단일 출처. 화면(영상.html)과 소리(audio.py)가 같이 읽는다. 120BPM = 0.5초 격자."""

FPS = 30
END = 30.0
W, H = 1080, 1920

# 장면 시작 시각(초). 전부 0.5초 격자 위
SCENES = dict(A=0.0, B=3.5, C=7.0, D1=14.0, D2=17.5, D3=21.0, E=24.5, F=27.5)

# 장면 안에서 소리가 붙는 순간(장면 시작 기준 상대 초)
REL = dict(
    A=dict(l1=0.25, l2=0.6, spec=[2.0, 2.25, 2.5]),
    B=dict(items=[0.5, 0.8, 1.1, 1.4], verdict=2.0),
    C=dict(bubbles=[0.7, 1.1, 1.5, 1.9], count=[2.7, 3.4], cap=3.4, turn=5.2),
    D1=dict(ellipse=1.0, ok=1.2, no=1.6),
    D2=dict(sticker=1.5),
    D3=dict(bars=[0.8, 1.0, 1.2], formula=2.0),
    E=dict(steps=[0.5, 0.9, 1.3]),
    F=dict(h1=0.15, spec=0.7, labels=[1.2, 1.45, 1.7]),
)


def payload() -> dict:
    return dict(scenes=SCENES, rel=REL, end=END)
