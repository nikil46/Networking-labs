
from pathlib import Path
import pandas as pd
import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="WSN DoS Detection Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
FIGURES_DIR = RESULTS_DIR / "final_figures"

# ==========================================
# DATA FILES
# ==========================================

COMPARISON_FILES = [
    RESULTS_DIR / "final_model_comparison_clean.csv",
    RESULTS_DIR / "final_model_comparison.csv",
]

FIGURE_FILES = {
    "Paper vs Implementation": "figure_1_paper_vs_implementation.png",
    "Macro F1-score": "figure_2_macro_f1.png",
    "Training Time": "figure_3_training_time.png",
    "Prediction Time": "figure_4_prediction_time.png",
    "18 vs 16 Features": "figure_5_feature_comparison.png",
}

CONFUSION_FILES = {
    "Decision Tree": "Decision Tree_confusion_matrix.png",
    "Random Forest": "Random_Forest_confusion_matrix.png",
    "XGBoost": "XGBoost_confusion_matrix.png",
    "KNN": "KNN_confusion_matrix.png",
}

MODEL_ORDER = [
    "Decision Tree",
    "Random Forest",
    "XGBoost",
    "KNN",
]

# ==========================================
# HELPER FUNCTIONS
# ==========================================

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)


def find_file(filename):
    """
    Find files recursively, ignoring differences
    in spaces, underscores, hyphens and capitalization.
    """

    def normalize(name):
        return "".join(
            char.lower()
            for char in name
            if char.isalnum()
        )

    target = normalize(filename)

    for folder in [RESULTS_DIR, BASE_DIR]:
        if not folder.exists():
            continue

        for path in folder.rglob("*"):
            if path.is_file():
                if normalize(path.name) == target:
                    return path

    return None


def load_comparison():
    for path in COMPARISON_FILES:
        if path.is_file():
            try:
                df = load_csv(path)
                df.columns = df.columns.str.strip()

                # Handle old comparison CSV column names.
                rename_map = {
                    "Macro_F1_x": "Macro_F1",
                    "Training_Time_x": "Training_Time",
                    "Prediction_Time_x": "Prediction_Time",
                }

                df = df.rename(columns=rename_map)

                # Remove duplicate column names.
                df = df.loc[:, ~df.columns.duplicated()]

                if "Model" not in df.columns:
                    continue

                return df

            except Exception as exc:
                st.error(f"Could not read {path.name}: {exc}")

    return pd.DataFrame()


def show_image(filename, caption=None):
    path = find_file(filename)

    if path:
        st.image(
            str(path),
            caption=caption or filename,
            width="stretch"
        )
    else:
        st.warning(f"Image not found: {filename}")


def show_download(path):
    try:
        with open(path, "rb") as file:
            st.download_button(
                label=f"Download {path.name}",
                data=file.read(),
                file_name=path.name,
                mime=(
                    "text/csv"
                    if path.suffix.lower() == ".csv"
                    else "application/octet-stream"
                ),
                key=str(path)
            )
    except OSError as exc:
        st.warning(f"Cannot download {path.name}: {exc}")


# ==========================================
# LOAD RESULTS
# ==========================================

comparison = load_comparison()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🛡️ WSN-DoS-ML")
st.sidebar.caption("M.Tech Project Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Performance Metrics",
        "Paper Comparison",
        "Final Graphs",
        "Confusion Matrix",
        "Dataset Analysis",
        "Results & Downloads",
        "Attack Detection (Step 31)",
    ]
)

st.sidebar.divider()
st.sidebar.success("Baseline experiments completed")
st.sidebar.caption("Results loaded from saved experiment files.")

# ==========================================
# OVERVIEW
# ==========================================

if page == "Overview":

    st.title("Wireless Sensor Network DoS Attack Detection")
    st.subheader("Machine Learning-Based Intrusion Detection")

    st.write(
        "This dashboard presents experimental results "
        "for detecting Denial-of-Service attacks in "
        "Wireless Sensor Networks using the WSN-DS dataset."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Dataset Records", "374,661")
    c2.metric("Selected Features", "16")
    c3.metric("Attack Classes", "5")
    c4.metric("ML Models", "4")

    st.divider()

    st.subheader("Machine Learning Models")

    st.write(
        "Decision Tree, Random Forest, XGBoost, "
        "and K-Nearest Neighbors."
    )

    st.subheader("Attack Categories")

    st.write(
        "Normal, Blackhole, Grayhole, Flooding, and TDMA."
    )

    st.subheader("Evaluation Methodology")

    st.write(
        "Stratified 10-fold cross-validation with "
        "accuracy, macro F1-score, accuracy standard "
        "deviation, training time, and prediction time."
    )

    if not comparison.empty and "Accuracy" in comparison.columns:

        best = comparison.loc[
            pd.to_numeric(
                comparison["Accuracy"],
                errors="coerce"
            ).idxmax()
        ]

        st.subheader("Best Performing Model")

        a, b = st.columns(2)

        a.metric("Model", str(best["Model"]))
        b.metric(
            "Accuracy",
            f"{float(best['Accuracy']):.4f}%"
        )

    st.info(
        "The baseline replication is complete. "
        "The published Gini weights were not "
        "independently reproduced."
    )

# ==========================================
# PERFORMANCE METRICS
# ==========================================

elif page == "Performance Metrics":

    st.title("Performance Metrics")

    if comparison.empty:
        st.error("Final model comparison CSV not found.")

    else:
        available_models = comparison["Model"].dropna().tolist()

        selected_model = st.selectbox(
            "Select Model",
            available_models
        )

        row = comparison[
            comparison["Model"] == selected_model
        ].iloc[0]

        st.subheader(f"{selected_model} Performance")

        metric_columns = [
            ("Accuracy", "Accuracy", "%", 4),
            ("Macro F1-score", "Macro_F1", "", 4),
            ("Accuracy Std", "Accuracy_Std", "", 4),
            ("Training Time", "Training_Time", " s", 4),
            ("Prediction Time", "Prediction_Time", " s", 4),
        ]

        cols = st.columns(3)

        for i, (label, column, suffix, digits) in enumerate(
            metric_columns
        ):
            if column in comparison.columns:
                value = pd.to_numeric(
                    row[column],
                    errors="coerce"
                )

                if pd.notna(value):
                    cols[i % 3].metric(
                        label,
                        f"{value:.{digits}f}{suffix}"
                    )

        st.divider()
        st.subheader("Complete Performance Comparison")

        st.dataframe(
            comparison,
            width="stretch",
            hide_index=True
        )

        for label, filename in [
            ("Macro F1-score", FIGURE_FILES["Macro F1-score"]),
            ("Training Time", FIGURE_FILES["Training Time"]),
            ("Prediction Time", FIGURE_FILES["Prediction Time"]),
        ]:
            st.subheader(label)
            show_image(filename, label)

# ==========================================
# PAPER COMPARISON
# ==========================================

elif page == "Paper Comparison":

    st.title("Published Paper vs Our Implementation")

    if comparison.empty:
        st.error("Comparison CSV not found.")

    else:
        columns = [
            col for col in [
                "Model",
                "Accuracy",
                "Paper_Accuracy",
                "Difference_pp",
                "Macro_F1",
            ]
            if col in comparison.columns
        ]

        st.dataframe(
            comparison[columns],
            width="stretch",
            hide_index=True
        )

        st.subheader("Accuracy Comparison")

        show_image(
            FIGURE_FILES["Paper vs Implementation"],
            "Published Paper vs Reproduced Accuracy"
        )

        st.info(
            "Small accuracy differences may result from "
            "preprocessing, model settings, and evaluation "
            "details. Matching accuracy does not establish "
            "complete methodological reproduction."
        )

# ==========================================
# FINAL GRAPHS
# ==========================================

elif page == "Final Graphs":

    st.title("Final Experimental Graphs")

    selected_graph = st.selectbox(
        "Select Graph",
        list(FIGURE_FILES.keys())
    )

    show_image(
        FIGURE_FILES[selected_graph],
        selected_graph
    )

    st.divider()
    st.subheader("All Experimental Graphs")

    for title, filename in FIGURE_FILES.items():

        with st.expander(title):
            show_image(filename, title)

# ==========================================
# CONFUSION MATRIX - FIXED
# ==========================================

elif page == "Confusion Matrix":

    st.title("Confusion Matrix")

    st.write(
        "Confusion matrices show the relationship between "
        "actual attack classes and model predictions."
    )

    selected_model = st.selectbox(
        "Select Machine Learning Model",
        MODEL_ORDER
    )

    filename = CONFUSION_FILES[selected_model]

    st.subheader(f"{selected_model} Confusion Matrix")

    image_path = find_file(filename)

    if image_path is not None:

        st.image(
            str(image_path),
            caption=f"{selected_model} Confusion Matrix",
            width="stretch"
        )

        show_download(image_path)

    else:

        st.warning(
            f"Confusion matrix image not found: {filename}"
        )

        st.info(
            "Check that the image exists in the results folder."
        )

    st.divider()

    st.subheader("View All Confusion Matrices")

    for model, filename in CONFUSION_FILES.items():

        with st.expander(f"{model} Confusion Matrix"):
            show_image(
                filename,
                f"{model} Confusion Matrix"
            )

    st.caption(
        "These images are loaded from saved experiments. "
        "The dashboard does not retrain models."
    )

# ==========================================
# DATASET ANALYSIS
# ==========================================

elif page == "Dataset Analysis":

    st.title("WSN-DS Dataset Analysis")

    st.subheader("Dataset Information")

    c1, c2, c3 = st.columns(3)

    c1.metric("Records", "374,661")
    c2.metric("Original Features", "18")
    c3.metric("Selected Features", "16")

    st.subheader("Class Distribution")

    class_counts = pd.DataFrame({
        "Attack Type": [
            "Normal",
            "Grayhole",
            "Blackhole",
            "TDMA",
            "Flooding"
        ],
        "Count": [
            340066,
            14596,
            10049,
            6638,
            3312
        ]
    })

    st.dataframe(
        class_counts,
        hide_index=True,
        width="stretch"
    )

    st.bar_chart(
        class_counts.set_index("Attack Type")["Count"]
    )

    st.subheader("Feature Selection")

    st.write(
        "The paper's selected configuration uses 16 "
        "predictor features, excluding dist_CH_To_BS "
        "and DATA_R."
    )

    show_image(
        FIGURE_FILES["18 vs 16 Features"],
        "18 Features vs 16 Features"
    )

    st.warning(
        "The dataset is class-imbalanced. "
        "Macro F1-score and class-specific metrics "
        "should be considered alongside accuracy."
    )

# ==========================================
# RESULTS AND DOWNLOADS
# ==========================================

elif page == "Results & Downloads":

    st.title("Results & Downloads")

    st.write(
        "Download experimental results, figures, "
        "and comparison tables."
    )

    if not RESULTS_DIR.exists():

        st.error("Results directory does not exist.")

    else:

        files = sorted(
            [
                path for path in RESULTS_DIR.rglob("*")
                if path.is_file()
                and path.suffix.lower() in [
                    ".csv", ".png", ".pdf", ".txt", ".md"
                ]
            ]
        )

        st.metric("Available Result Files", len(files))

        file_type = st.selectbox(
            "Filter Files",
            ["All", "CSV", "PNG", "PDF", "TXT", "MD"]
        )

        if file_type != "All":
            files = [
                path for path in files
                if path.suffix.lower() == f".{file_type.lower()}"
            ]

        for path in files:

            relative_path = path.relative_to(RESULTS_DIR)

            with st.expander(str(relative_path)):

                if path.suffix.lower() == ".png":
                    st.image(str(path), width="stretch")

                elif path.suffix.lower() == ".csv":
                    try:
                        st.dataframe(
                            load_csv(path),
                            width="stretch"
                        )
                    except Exception as exc:
                        st.warning(str(exc))

                show_download(path)

# ==========================================
# STEP 31: PRACTICAL ATTACK DETECTION
# ==========================================

elif page == "Attack Detection (Step 31)":
    import io
    import joblib
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

    st.title("Practical DoS Attack Detection & Verification")
    st.caption("Offline classification of held-out or uploaded WSN-DS records; not live network monitoring.")
    bundle_path = BASE_DIR / "models" / "step31_decision_tree.joblib"
    if not bundle_path.is_file():
        st.error("Saved model not found. Run: python step31_train_verify.py")
        st.stop()

    @st.cache_resource
    def load_step31_model(path, modified):
        return joblib.load(path)  # Only load model files generated by your own trusted script.

    bundle = load_step31_model(str(bundle_path), bundle_path.stat().st_mtime)
    model = bundle["model"]
    features = bundle["features"]
    st.write("Model: **Decision Tree** | Features: **16** | Evaluation: **group-disjoint holdout**")
    default_test = BASE_DIR / "models" / "step31_unseen_test.csv"
    uploaded = st.file_uploader("Upload WSN-DS CSV (optional)", type=["csv"])
    if uploaded is None:
        if not default_test.exists():
            st.warning("No held-out test CSV found. Run the Step 31 training script first.")
            st.stop()
        df_test = pd.read_csv(default_test)
        st.info("Using the saved held-out test dataset (not used for model training).")
    else:
        df_test = pd.read_csv(uploaded)
        st.warning("Uploaded CSVs are not automatically guaranteed to be unseen. Verify their origin before claiming independent validation.")

    df_test.columns = df_test.columns.str.strip()
    if df_test.columns.duplicated().any():
        st.error("Duplicate column names detected.")
        st.stop()
    missing = [c for c in features if c not in df_test.columns]
    if missing:
        st.error(f"Missing required features: {missing}")
        st.stop()
    X_input = df_test.loc[:, features].copy()
    try:
        for c in features:
            X_input[c] = pd.to_numeric(X_input[c], errors="raise")
        if X_input.isna().any().any():
            raise ValueError("Input contains missing feature values")
        predicted = model.predict(X_input)
    except (ValueError, TypeError) as exc:
        st.error(f"Invalid input features: {exc}")
        st.stop()

    output = pd.DataFrame({"Predicted Attack Type": predicted})
    output["Detection"] = output["Predicted Attack Type"].apply(
        lambda x: "Normal" if x == "Normal" else "Attack"
    )
    a, b, c = st.columns(3)
    a.metric("Records classified", len(output))
    b.metric("Predicted attacks", int((output["Detection"] == "Attack").sum()))
    c.metric("Predicted normal", int((output["Detection"] == "Normal").sum()))
    st.subheader("Predictions")
    st.dataframe(output.head(200), hide_index=True, width="stretch")
    st.subheader("Predicted class distribution")
    st.bar_chart(output["Predicted Attack Type"].value_counts())

    if "Attack type" in df_test.columns:
        actual = df_test["Attack type"].astype(str)
        labels = sorted(set(actual.unique()).union(set(map(str, predicted))))
        st.subheader("Verification against ground truth")
        st.metric("Accuracy on this input", f"{accuracy_score(actual, predicted):.4%}")
        report = classification_report(actual, predicted, labels=labels,
                                       output_dict=True, zero_division=0)
        st.dataframe(pd.DataFrame(report).transpose(), width="stretch")
        matrix = pd.DataFrame(confusion_matrix(actual, predicted, labels=labels),
                              index=labels, columns=labels)
        st.write("Confusion matrix — rows: actual, columns: predicted")
        st.dataframe(matrix, width="stretch")
        output.insert(0, "Actual Attack Type", actual.to_numpy())
        output["Correct"] = output["Actual Attack Type"] == output["Predicted Attack Type"]
    else:
        st.info("No 'Attack type' label column: predictions are possible, but accuracy cannot be verified.")

    st.download_button("Download predictions CSV", output.to_csv(index=False).encode("utf-8"),
                       file_name="step31_predictions.csv", mime="text/csv")

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "WSN DoS Detection ML | M.Tech Research Project | "
    "Experimental Results Dashboard"
)
