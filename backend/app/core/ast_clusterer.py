"""
AST-based test clustering using hybrid vector/hash approach
"""

import ast
import hashlib
from typing import List, Dict, Any, Optional

import numpy as np
from loguru import logger
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

from app.utils.exceptions import ClusteringError


class ASTClusterer:
    """
    Clusters test functions using AST-based features
    Supports both vector-based (DBSCAN) and hash-based clustering
    """

    def __init__(self, method: str = "vector", eps: float = 0.3, min_samples: int = 2):
        """
        Initialize clusterer

        Args:
            method: Clustering method ("vector" or "hash")
            eps: DBSCAN epsilon parameter
            min_samples: DBSCAN min_samples parameter
        """
        self.method = method
        self.eps = eps
        self.min_samples = min_samples
        self.cluster_labels: Optional[np.ndarray] = None
        self.features: Optional[np.ndarray] = None

    def cluster_tests(self, tests: List[str]) -> Dict[int, List[int]]:
        """
        Cluster tests into groups

        Args:
            tests: List of test function code strings

        Returns:
            Dictionary mapping cluster_id to list of test indices
        """
        if not tests:
            return {}

        logger.info(f"Clustering {len(tests)} tests using {self.method} method")

        if self.method == "vector":
            return self._cluster_by_vector(tests)
        elif self.method == "hash":
            return self._cluster_by_hash(tests)
        else:
            raise ClusteringError(f"Unknown clustering method: {self.method}")

    def _cluster_by_vector(self, tests: List[str]) -> Dict[int, List[int]]:
        """Cluster using DBSCAN on AST feature vectors"""
        try:
            # Extract features
            features = []
            for test in tests:
                feature_vector = self._extract_ast_features(test)
                features.append(feature_vector)

            self.features = np.array(features)

            # Normalize features
            scaler = StandardScaler()
            normalized_features = scaler.fit_transform(self.features)

            # Apply DBSCAN
            dbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples, metric='euclidean')
            self.cluster_labels = dbscan.fit_predict(normalized_features)

            # Organize results
            clusters = {}
            for idx, label in enumerate(self.cluster_labels):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(idx)

            n_clusters = len([c for c in clusters.keys() if c != -1])
            n_noise = len(clusters.get(-1, []))

            logger.info(f"DBSCAN clustering: {n_clusters} clusters, {n_noise} noise points")

            return clusters

        except Exception as e:
            logger.error(f"Vector clustering failed: {e}", exc_info=True)
            raise ClusteringError(f"Vector clustering failed: {str(e)}")

    def _cluster_by_hash(self, tests: List[str]) -> Dict[int, List[int]]:
        """Cluster using structural hash comparison"""
        try:
            # Generate structural hashes
            hashes = []
            for test in tests:
                struct_hash = self._compute_structural_hash(test)
                hashes.append(struct_hash)

            # Group by hash
            hash_to_indices = {}
            for idx, hash_val in enumerate(hashes):
                if hash_val not in hash_to_indices:
                    hash_to_indices[hash_val] = []
                hash_to_indices[hash_val].append(idx)

            # Convert to cluster format (assign cluster IDs)
            clusters = {}
            cluster_id = 0

            for hash_val, indices in hash_to_indices.items():
                if len(indices) >= self.min_samples:
                    clusters[cluster_id] = indices
                    cluster_id += 1
                else:
                    # Singleton or small groups -> noise
                    if -1 not in clusters:
                        clusters[-1] = []
                    clusters[-1].extend(indices)

            n_clusters = len([c for c in clusters.keys() if c != -1])
            n_noise = len(clusters.get(-1, []))

            logger.info(f"Hash clustering: {n_clusters} clusters, {n_noise} noise points")

            return clusters

        except Exception as e:
            logger.error(f"Hash clustering failed: {e}", exc_info=True)
            raise ClusteringError(f"Hash clustering failed: {str(e)}")

    def _extract_ast_features(self, test_code: str) -> List[float]:
        """
        Extract numerical features from AST for vectorization

        Features:
        - Number of assertions
        - Number of function calls
        - Number of comparisons
        - Number of literals
        - Tree depth
        - Number of try/except blocks
        - Number of pytest.raises calls
        - Number of assignments
        """
        try:
            tree = ast.parse(test_code)

            features = {
                "assertions": 0,
                "function_calls": 0,
                "comparisons": 0,
                "literals": 0,
                "depth": 0,
                "try_except": 0,
                "pytest_raises": 0,
                "assignments": 0
            }

            # Walk the AST
            for node in ast.walk(tree):
                if isinstance(node, ast.Assert):
                    features["assertions"] += 1
                elif isinstance(node, ast.Call):
                    features["function_calls"] += 1
                    # Check for pytest.raises
                    if self._is_pytest_raises(node):
                        features["pytest_raises"] += 1
                elif isinstance(node, ast.Compare):
                    features["comparisons"] += 1
                elif isinstance(node, (ast.Constant, ast.Num, ast.Str)):
                    features["literals"] += 1
                elif isinstance(node, ast.Try):
                    features["try_except"] += 1
                elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                    features["assignments"] += 1

            # Calculate tree depth
            features["depth"] = self._calculate_ast_depth(tree)

            return list(features.values())

        except:
            # Return zero vector on parse error
            return [0.0] * 8

    def _compute_structural_hash(self, test_code: str) -> str:
        """
        Compute structural hash based on AST structure
        Ignores variable names and literal values
        """
        try:
            tree = ast.parse(test_code)

            # Generate structure signature
            structure = []

            for node in ast.walk(tree):
                node_type = type(node).__name__
                structure.append(node_type)

                # Add important structural elements
                if isinstance(node, ast.Call):
                    if hasattr(node.func, 'attr'):
                        structure.append(node.func.attr)
                elif isinstance(node, ast.Compare):
                    structure.append(str([type(op).__name__ for op in node.ops]))

            # Hash the structure
            structure_str = '|'.join(structure)
            return hashlib.md5(structure_str.encode()).hexdigest()

        except:
            # Return unique hash on parse error
            return hashlib.md5(test_code.encode()).hexdigest()

    def _is_pytest_raises(self, node: ast.Call) -> bool:
        """Check if a Call node is pytest.raises"""
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "raises":
                if isinstance(node.func.value, ast.Name):
                    if node.func.value.id == "pytest":
                        return True
        return False

    def _calculate_ast_depth(self, node: ast.AST, depth: int = 0) -> int:
        """Calculate maximum depth of AST"""
        max_depth = depth

        for child in ast.iter_child_nodes(node):
            child_depth = self._calculate_ast_depth(child, depth + 1)
            max_depth = max(max_depth, child_depth)

        return max_depth

    def get_cluster_info(
            self,
            cluster_id: int,
            tests: List[str],
            cluster_map: Dict[int, List[int]]
    ) -> Dict[str, Any]:
        """
        Get detailed information about a cluster

        Args:
            cluster_id: Cluster identifier
            tests: All test codes
            cluster_map: Cluster mapping

        Returns:
            Cluster information dictionary
        """
        if cluster_id not in cluster_map:
            return {}

        indices = cluster_map[cluster_id]
        cluster_tests = [tests[i] for i in indices]

        info = {
            "cluster_id": cluster_id,
            "size": len(indices),
            "test_indices": indices,
            "tests": cluster_tests
        }

        # Add representative test (shortest one)
        if cluster_tests:
            representative = min(cluster_tests, key=len)
            info["representative_test"] = representative

        return info
