"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.
"""

SCENARIOS = [
    # ── Criterion 1: False Positives (10 pieces of own writing) ─────────────
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": [
            (
                "I spent Saturday morning out in the garage trying to troubleshoot a lawnmower "
                "that refused to start after sitting idle all winter. The carburetor was completely "
                "gummed up with stale fuel, and I had to take the whole assembly apart piece by "
                "piece, scrubbing the jets with wire until my knuckles were sore and smelled of gasoline."
            ),
            (
                "Baking sourdough bread is mostly a lesson in patience and ambient room temperature. "
                "If the kitchen is too drafty, the dough barely rises even after six hours; if it's too warm, "
                "the fermentation runs wild and you end up with a sticky, overproofed mess that puddles "
                "on the parchment paper."
            ),
            (
                "We ducked into a small diner just as the sky turned dark and unleashed a sudden downpour. "
                "The booth had cracked vinyl tape on the seat and the coffee tasted slightly burnt, but watching "
                "the rain hammer the neon sign outside made the whole afternoon feel oddly cozy."
            ),
            (
                "I still prefer physical paperback books over reading on an e-reader, even if they take up "
                "half my backpack. There is something deeply satisfying about dog-earing a page, feeling the "
                "weight shift from right hand to left as you read, and finding random receipts from three years ago."
            ),
            (
                "Learning fingerstyle guitar has been surprisingly humbling. My ring finger on my right hand "
                "simply refuses to move independently of the middle one, so every attempt at Travis picking "
                "sounds like a clumsy stumble until muscle memory finally takes over after weeks of practice."
            ),
            (
                "While hiking along the ridge trail last October, the wind picked up so fast it nearly knocked "
                "my hat off into the canyon. The valley below was blanketed in a sea of gold and crimson leaves, "
                "and for about ten minutes, nobody in our group said a single word."
            ),
            (
                "My morning coffee ritual hasn't changed in seven years: grind twenty grams of dark roast beans, "
                "pre-wet the filter to rinse the paper taste, and pour three hundred grams of water in slow, "
                "steady circles while the kitchen fills with steam before anyone else wakes up."
            ),
            (
                "The stray calico cat that lives under our deck has a remarkably stubborn routine. Exactly at "
                "dusk, she sits on the top porch step, stares directly through the glass door without blinking, "
                "and lets out a single indignant meow until someone brings out a dish of tuna."
            ),
            (
                "Walking the beach at low tide during winter is when you find the best sea glass. The summer "
                "crowds are long gone, the damp sand is firm under your boots, and pieces of frosted green and "
                "amber glass glint against the wet pebbles like miniature treasures."
            ),
            (
                "There is a unique kind of exhaustion that comes from hunting an off-by-one bug at two in the "
                "morning. You stare at the loop boundary until the variables stop making sense, only to realize "
                "after three cups of tea that you used less-than instead of less-than-or-equal."
            ),
        ],
    },

    # ── Criterion 2: Score Spread (5 human + 5 AI inputs) ────────────────────
    {
        "name": "score spread",
        "criterion": 2,
        "texts": [
            # 5 clearly human texts
            (
                "No way. When I finally dragged myself out of bed at four in the morning, shivering and completely "
                "bewildered, I discovered a family of raccoons having an absolute feast in my trash; they didn't "
                "even flinch when I yelled. Honestly, who can blame them?"
            ),
            (
                "We had three flat tires on that trip! Three! The first near Flagstaff, the second right outside "
                "Barstow, and the third when we pulled into my brother's gravel driveway. At that point, all we "
                "could do was sit on the curb and laugh until our stomachs hurt."
            ),
            (
                "I told Grandma her soup was spicy. She looked at me over her glasses, shook her head, and told "
                "me that back in her village, babies drank this broth for teething. I drank the whole bowl anyway, "
                "sweating through my sweater."
            ),
            (
                "The old typewriter key kept sticking on the letter 'e'. You'd type along happily, look down at "
                "the paper, and discover half your sentences looked like coded telegrams missing vowels. It took "
                "an entire afternoon with WD-40 and a toothbrush to get it unstuck."
            ),
            (
                "Look, nobody enjoys folding fitted sheets. You start with good intentions, tucking corners into "
                "corners, and by step four you've rolled the entire thing into an uneven cotton ball and shoved "
                "it into the linen closet hoping nobody looks inside."
            ),
            # 5 clearly AI texts
            (
                "Artificial intelligence technologies have experienced exponential advancement over the past "
                "decade, profoundly transforming diverse sectors such as healthcare diagnostics, autonomous "
                "transportation, and algorithmic financial forecasting through computational optimization."
            ),
            (
                "In conclusion, the implementation of sustainable renewable energy infrastructure represents a "
                "crucial paradigm shift, mitigating harmful carbon emissions while concurrently enhancing grid "
                "reliability and fostering long-term economic development across metropolitan regions."
            ),
            (
                "To comprehend deep neural network architectures, one must systematically examine the mathematical "
                "principles of backpropagation, wherein partial derivatives of the objective loss function are "
                "recursively propagated across sequential hidden layers via the chain rule."
            ),
            (
                "Effective enterprise leadership necessitates clear communication channels, transparent resource "
                "allocation, and proactive risk mitigation strategies designed to optimize cross-functional team "
                "performance and facilitate continuous operational refinement."
            ),
            (
                "Photosynthesis represents a foundational biochemical process whereby terrestrial plants and "
                "cyanobacteria harness solar radiation to convert carbon dioxide and water into complex organic "
                "compounds, thereby sustaining terrestrial biodiversity and atmospheric oxygen levels."
            ),
        ],
    },

    # ── Criterion 3: Label Coverage & Borderline (10 inputs) ─────────────────
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            # 5 borderline inputs (0.40 - 0.60, targeting 'unsure')
            (
                "The study evaluated three distinct methods of water purification across rural communities. "
                "While solar distillation demonstrated modest efficiency, ceramic filtration proved substantially "
                "more reliable during periods of heavy seasonal runoff, though community adoption varied."
            ),
            (
                "Our experiment measured heat transfer coefficients across several metal alloys. Although copper "
                "demonstrated higher thermal conductivity under static conditions, aluminum provided superior "
                "durability when subjected to cyclic thermal stress over extended observation periods."
            ),
            (
                "Modern distributed databases must balance consistency guarantees with system availability. "
                "By implementing optimistic concurrency control, engineers can reduce lock contention, though "
                "network partitions inevitably introduce latency spikes during partition reconciliation."
            ),
            (
                "The conference panel discussed urban transit modernization strategies. Panelists noted that "
                "electrifying municipal bus fleets reduces emissions significantly, but charging infrastructure "
                "requires substantial capital expenditure and utility grid upgrades."
            ),
            (
                "Evaluating soil samples from agricultural test plots revealed marked differences in microbial "
                "diversity. Plots treated with cover crops maintained higher nitrogen retention, whereas "
                "conventionally tilled soil suffered measurable topsoil loss following heavy autumn rains."
            ),
            # 2-3 high-confidence human inputs (< 0.35, targeting 'high-confidence human')
            (
                "Wait, you actually touched it? Gross! I wouldn't go near that creepy abandoned barn for all the "
                "money in the world, especially with the weird scratching sounds coming from the loft."
            ),
            (
                "My old boots finally blew out at the heel yesterday. Ten years of hiking, muddy riverbanks, "
                "and snowdrifts, and they gave up on a flat sidewalk walking to the grocery store. Total betrayal."
            ),
            # 2-3 high-confidence AI inputs (> 0.65, targeting 'high-confidence AI')
            (
                "Furthermore, machine learning frameworks utilize gradient descent algorithms to systematically "
                "minimize empirical risk functions across high-dimensional parameter spaces, ensuring convergence "
                "toward optimal model representations."
            ),
            (
                "Consequently, the adoption of standardized protocol architectures streamlines data interoperability, "
                "establishing robust benchmarks for cybersecurity compliance and ensuring verifiable system integrity."
            ),
        ],
    },

    # ── Criterion 4: The Appeal Path (5 test submissions) ────────────────────
    {
        "name": "appeal path",
        "criterion": 4,
        "texts": [
            (
                "I drafted this historical overview on 19th-century maritime trade as an assigned research paper, "
                "relying heavily on primary ship manifests and port records from Boston harbor archives."
            ),
            (
                "This technical analysis of municipal wastewater filtration was written following our civil engineering "
                "field inspection, using data collected directly from our flow rate monitoring instruments."
            ),
            (
                "My submission covers comparative literature between Victorian poetry and romantic prose, written "
                "specifically to adhere to our department's stylistic formatting guidelines and rubrics."
            ),
            (
                "I wrote this lab summary describing the crystallization kinetics of sodium chloride solutions, "
                "incorporating our recorded temperature curves and photographic evidence from the microscope."
            ),
            (
                "This philosophy reflection examines ethical frameworks in medical triage, drafted as my final "
                "course thesis using citations from contemporary bioethics journals."
            ),
        ],
    },

    # ── Criterion 5: Bad Input Handling (4 malformed bodies) ─────────────────
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "overflow " * 50001, "creator_id": "eval_bad_huge"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
