import matplotlib.pyplot as plt

levels = ["L1", "L2", "L3", "L4", "L5", "L6"]

gpt4o_indirect = [12.0, 7.0, 5.0, 2.0, 1.0, 0.5]
gpt41_indirect = [18.0, 12.0, 7.0, 9.0, 2.0, 0.8]
claude_indirect = [8.0, 3.0, 2.5, 0.9, 0.0, 0.0]

plt.figure(figsize=(10, 6))

plt.plot(levels, gpt4o_indirect, marker="o", linewidth=2.5, label="GPT-4o-mini")
plt.plot(levels, gpt41_indirect, marker="o", linewidth=2.5, label="GPT-4.1-mini")
plt.plot(levels, claude_indirect, marker="o", linewidth=2.5, label="Claude Sonnet 4.6")

plt.title("ASR pre nepriame útoky podľa úrovní obrany", fontsize=15, pad=15)
plt.xlabel("Úroveň obrany", fontsize=12)
plt.ylabel("ASR (%)", fontsize=12)

plt.grid(True, linestyle="--", alpha=0.4)
plt.legend(frameon=False)

plt.tight_layout()
plt.savefig("graf_nepriame_utoky.png", dpi=300, bbox_inches="tight")
plt.show()