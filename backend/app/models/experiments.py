"""
Experiment configuration models for batch testing and ablation studies
"""

from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class ExperimentType(str, Enum):
    """Experiment configuration types"""
    FULL_SYSTEM = "full_system"
    NO_ROLES = "no_roles"  # Ablation 1
    SINGLE_MODEL = "single_model"  # Ablation 2
    NO_CLUSTERING = "no_clustering"  # Ablation 3
    NO_SYNTHESIS = "no_synthesis"  # Ablation 4


class ExperimentConfig(BaseModel):
    """Configuration for a single experiment"""

    experiment_id: str = Field(
        ...,
        description="Unique experiment identifier"
    )

    experiment_type: ExperimentType = Field(
        ...,
        description="Type of experiment"
    )

    description: str = Field(
        ...,
        description="Human-readable description"
    )

    # Model configuration
    models: Optional[List[str]] = Field(
        None,
        description="Models to use (None = all models)"
    )

    # Role configuration
    roles: Optional[List[str]] = Field(
        None,
        description="Roles to use (None = all roles, empty list = no roles)"
    )

    use_role_personas: bool = Field(
        default=True,
        description="Whether to use role-specific prompts"
    )

    # Clustering configuration
    enable_clustering: bool = Field(
        default=True,
        description="Enable test clustering"
    )

    clustering_method: str = Field(
        default="vector",
        description="Clustering method: 'vector' or 'hash'"
    )

    eps: float = Field(
        default=0.3,
        ge=0.1,
        le=1.0,
        description="DBSCAN epsilon parameter"
    )

    min_samples: int = Field(
        default=2,
        ge=1,
        le=5,
        description="DBSCAN min_samples parameter"
    )

    # Synthesis configuration
    enable_synthesis: bool = Field(
        default=True,
        description="Enable test synthesis"
    )

    # Coverage configuration
    enable_coverage: bool = Field(
        default=True,
        description="Enable coverage analysis"
    )

    # ✅ NEW: Mutation testing configuration
    enable_mutation: bool = Field(
        default=True,
        description="Enable mutation testing (gold standard metric, can be slow)"
    )


class BatchResult(BaseModel):
    """Result for a single function in batch processing"""

    function_name: str
    experiment_id: str
    success: bool
    error_message: Optional[str] = None

    # ✅ NEW: Syntax validation
    is_runnable: Optional[bool] = None
    syntax_error: Optional[str] = None

    # Generation statistics
    total_raw_tests: Optional[int] = None
    total_clusters: Optional[int] = None
    noise_tests: Optional[int] = None
    final_tests_count: Optional[int] = None

    # Coverage results
    coverage_percentage: Optional[float] = None
    branch_coverage_percentage: Optional[float] = None
    passed_tests: Optional[int] = None
    failed_tests: Optional[int] = None
    success_rate: Optional[float] = None

    # Quality metrics
    assertion_density: Optional[float] = None
    diversity_score: Optional[float] = None
    edge_case_score: Optional[float] = None
    avg_test_complexity: Optional[float] = None
    test_loc: Optional[int] = None
    source_loc: Optional[int] = None
    loc_efficiency: Optional[float] = None
    duplication_rate: Optional[float] = None
    exception_coverage_rate: Optional[float] = None

    # Mutation testing metrics
    mutation_score: Optional[float] = None
    total_mutants: Optional[int] = None
    killed_mutants: Optional[int] = None
    survived_mutants: Optional[int] = None

    # Timing
    total_duration_seconds: Optional[float] = None
    llm_duration_seconds: Optional[float] = None
    clustering_duration_seconds: Optional[float] = None
    synthesis_duration_seconds: Optional[float] = None
    coverage_duration_seconds: Optional[float] = None

    # Full outputs
    final_tests_code: Optional[str] = None
    cluster_details: Optional[str] = None  # JSON string



def get_experiment_configs() -> List[ExperimentConfig]:
    """Get all 5 experiment configurations"""

    return [
        # Experiment 1: Full System (Baseline)
        ExperimentConfig(
            experiment_id="exp_1_full_system",
            experiment_type=ExperimentType.FULL_SYSTEM,
            description="Full system with all features enabled",
            models=None,  # All models
            roles=None,  # All roles
            use_role_personas=True,
            enable_clustering=True,
            clustering_method="vector",
            eps=0.3,
            min_samples=2,
            enable_synthesis=True,
            enable_coverage=True,
            enable_mutation=True  # ✅ NEW
        ),

        # Experiment 2: Ablation 1 - No Role Personas
        ExperimentConfig(
            experiment_id="exp_2_no_roles",
            experiment_type=ExperimentType.NO_ROLES,
            description="Ablation 1: Generic prompts without role-specific personas",
            models=None,  # All models
            roles=[],  # Empty list = no roles (generic prompts)
            use_role_personas=False,
            enable_clustering=True,
            clustering_method="vector",
            eps=0.3,
            min_samples=2,
            enable_synthesis=True,
            enable_coverage=True,
            enable_mutation=True  # ✅ NEW
        ),

        # Experiment 3: Ablation 2 - Single Model
        ExperimentConfig(
            experiment_id="exp_3_single_model",
            experiment_type=ExperimentType.SINGLE_MODEL,
            description="Ablation 2: Single model (Gemini 2.0 Flash) with all roles",
            models=["gemini-2.0-flash"],  # Only Gemini
            roles=None,  # All roles
            use_role_personas=True,
            enable_clustering=True,
            clustering_method="vector",
            eps=0.3,
            min_samples=2,
            enable_synthesis=True,
            enable_coverage=True,
            enable_mutation=True  # ✅ NEW
        ),

        # Experiment 4: Ablation 3 - No Clustering
        ExperimentConfig(
            experiment_id="exp_4_no_clustering",
            experiment_type=ExperimentType.NO_CLUSTERING,
            description="Ablation 3: No clustering, all tests treated as one group",
            models=None,  # All models
            roles=None,  # All roles
            use_role_personas=True,
            enable_clustering=False,
            clustering_method="vector",  # Not used
            eps=0.3,
            min_samples=2,
            enable_synthesis=True,
            enable_coverage=True,
            enable_mutation=True  # ✅ NEW
        ),

        # Experiment 5: Ablation 4 - No Synthesis
        ExperimentConfig(
            experiment_id="exp_5_no_synthesis",
            experiment_type=ExperimentType.NO_SYNTHESIS,
            description="Ablation 4: Random selection instead of synthesis",
            models=None,  # All models
            roles=None,  # All roles
            use_role_personas=True,
            enable_clustering=True,
            clustering_method="vector",
            eps=0.3,
            min_samples=2,
            enable_synthesis=False,
            enable_coverage=True,
            enable_mutation=True  # ✅ NEW
        ),
    ]
