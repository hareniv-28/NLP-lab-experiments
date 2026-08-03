from importlib import import_module
from pathlib import Path

plt = import_module("matplotlib.pyplot")
text_mod = import_module("sklearn.feature_extraction.text")
CountVectorizer = text_mod.CountVectorizer
decomp_mod = import_module("sklearn.decomposition")
LatentDirichletAllocation = decomp_mod.LatentDirichletAllocation
manifold_mod = import_module("sklearn.manifold")
TSNE = manifold_mod.TSNE

reviews = []


def read_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Please enter a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")


n = read_positive_int("Enter number of reviews: ")

for i in range(n):
    reviews.append(input("Enter review: "))

vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(reviews)

lda = LatentDirichletAllocation(n_components=2, random_state=42)
lda.fit(X)

words = vectorizer.get_feature_names_out()

print("\nTopics:")
for i, topic in enumerate(lda.components_):
    print("\nTopic", i + 1)
    top_words = topic.argsort()[-5:]
    for j in top_words:
        print(words[j])

X_dense = X.toarray()

perplexity = min(5, max(1, n - 1))
tsne = TSNE(n_components=2, random_state=42, perplexity=perplexity)
X_tsne = tsne.fit_transform(X_dense)

print("\nt-SNE Coordinates:")
for i, point in enumerate(X_tsne):
    print("Review", i + 1, ":", point)

plt.scatter(X_tsne[:, 0], X_tsne[:, 1])

for i in range(len(reviews)):
    plt.text(X_tsne[i, 0], X_tsne[i, 1], "R" + str(i + 1))

plt.title("t-SNE Visualization of Customer Reviews")
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")
plt.tight_layout()
plot_path = Path(__file__).resolve().parent / "plot.png"
plt.savefig(plot_path, dpi=200, bbox_inches="tight")
plt.close()