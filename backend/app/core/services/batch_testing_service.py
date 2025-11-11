"""
Batch Testing Service - Process multiple functions from CSV
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

import pandas as pd
from loguru import logger

from app.core.services.test_generation_service import TestGenerationService
from app.models.experiments import ExperimentConfig
from app.models.requests import TestGenerationRequest


class BatchTestingService:
    """Service for batch processing test generation experiments"""

    def __init__(self):
        self.service = TestGenerationService()

    async def process_csv_batch(
            self,
            csv_path: str,
            experiment_config: ExperimentConfig,
            output_dir: str,
            max_concurrent: int = 3
    ) -> pd.DataFrame:
        """
        Process a CSV file of Python functions through test generation pipeline
        """
        logger.info(f"Starting batch processing: {experiment_config.experiment_id}")
        logger.info(f"Input CSV: {csv_path}")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Mutation testing: {'ENABLED' if experiment_config.enable_mutation else 'DISABLED'}")

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Read CSV
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(df)} functions from CSV")
        except Exception as e:
            logger.error(f"Failed to read CSV: {e}")
            raise

        # Validate CSV structure
        required_columns = ['function_code']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")

        # ✅ Add result columns (including syntax check AND branch coverage details)
        result_columns = [
            f'{experiment_config.experiment_id}_success',
            f'{experiment_config.experiment_id}_is_runnable',  # ✅ Syntax validation
            f'{experiment_config.experiment_id}_syntax_error',
            f'{experiment_config.experiment_id}_total_tests',
            f'{experiment_config.experiment_id}_clusters',
            f'{experiment_config.experiment_id}_final_tests',

            # Coverage metrics
            f'{experiment_config.experiment_id}_line_coverage_%',
            f'{experiment_config.experiment_id}_branch_coverage_%',
            f'{experiment_config.experiment_id}_total_branches',      # ✅ NEW
            f'{experiment_config.experiment_id}_covered_branches',    # ✅ NEW
            f'{experiment_config.experiment_id}_has_branches',        # ✅ NEW

            # Test execution
            f'{experiment_config.experiment_id}_passed_tests',
            f'{experiment_config.experiment_id}_failed_tests',
            f'{experiment_config.experiment_id}_test_success_rate_%',

            # Quality metrics
            f'{experiment_config.experiment_id}_assertion_density',
            f'{experiment_config.experiment_id}_diversity_score',
            f'{experiment_config.experiment_id}_edge_case_score',
            f'{experiment_config.experiment_id}_avg_test_complexity',

            # Standard metrics
            f'{experiment_config.experiment_id}_test_loc',
            f'{experiment_config.experiment_id}_source_loc',
            f'{experiment_config.experiment_id}_loc_efficiency',
            f'{experiment_config.experiment_id}_duplication_rate_%',
            f'{experiment_config.experiment_id}_exception_coverage_%',

            # Mutation testing metrics
            f'{experiment_config.experiment_id}_mutation_score_%',
            f'{experiment_config.experiment_id}_total_mutants',
            f'{experiment_config.experiment_id}_killed_mutants',
            f'{experiment_config.experiment_id}_survived_mutants',

            # Timing
            f'{experiment_config.experiment_id}_duration_s',

            # Output
            f'{experiment_config.experiment_id}_tests_code',
            f'{experiment_config.experiment_id}_cluster_info',
            f'{experiment_config.experiment_id}_error'
        ]

        for col in result_columns:
            if col not in df.columns:
                df[col] = None

        # Process functions
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_row(index: int, row: pd.Series):
            async with semaphore:
                return await self._process_single_function(
                    index=index,
                    function_code=row['function_code'],
                    function_name=row.get('function_name'),
                    experiment_config=experiment_config
                )

        # Create tasks
        tasks = [
            process_row(idx, row)
            for idx, row in df.iterrows()
        ]

        # Execute with progress
        results = []
        for i, task in enumerate(asyncio.as_completed(tasks)):
            result = await task
            results.append(result)
            logger.info(f"Progress: {i+1}/{len(tasks)} functions completed")

        # Update DataFrame with results
        for result in results:
            idx = result['index']
            exp_id = experiment_config.experiment_id

            df.at[idx, f'{exp_id}_success'] = result['success']
            df.at[idx, f'{exp_id}_is_runnable'] = result.get('is_runnable')
            df.at[idx, f'{exp_id}_syntax_error'] = result.get('syntax_error')
            df.at[idx, f'{exp_id}_total_tests'] = result.get('total_raw_tests')
            df.at[idx, f'{exp_id}_clusters'] = result.get('total_clusters')
            df.at[idx, f'{exp_id}_final_tests'] = result.get('final_tests_count')

            # Coverage (with new branch details)
            df.at[idx, f'{exp_id}_line_coverage_%'] = result.get('coverage_percentage')
            df.at[idx, f'{exp_id}_branch_coverage_%'] = result.get('branch_coverage_percentage')
            df.at[idx, f'{exp_id}_total_branches'] = result.get('total_branches')        # ✅ NEW
            df.at[idx, f'{exp_id}_covered_branches'] = result.get('covered_branches')    # ✅ NEW
            df.at[idx, f'{exp_id}_has_branches'] = result.get('has_branches')            # ✅ NEW

            # Test execution
            df.at[idx, f'{exp_id}_passed_tests'] = result.get('passed_tests')
            df.at[idx, f'{exp_id}_failed_tests'] = result.get('failed_tests')
            df.at[idx, f'{exp_id}_test_success_rate_%'] = result.get('success_rate')

            # Quality metrics
            df.at[idx, f'{exp_id}_assertion_density'] = result.get('assertion_density')
            df.at[idx, f'{exp_id}_diversity_score'] = result.get('diversity_score')
            df.at[idx, f'{exp_id}_edge_case_score'] = result.get('edge_case_score')
            df.at[idx, f'{exp_id}_avg_test_complexity'] = result.get('avg_test_complexity')

            # Standard metrics
            df.at[idx, f'{exp_id}_test_loc'] = result.get('test_loc')
            df.at[idx, f'{exp_id}_source_loc'] = result.get('source_loc')
            df.at[idx, f'{exp_id}_loc_efficiency'] = result.get('loc_efficiency')
            df.at[idx, f'{exp_id}_duplication_rate_%'] = result.get('duplication_rate')
            df.at[idx, f'{exp_id}_exception_coverage_%'] = result.get('exception_coverage_rate')

            # Mutation metrics
            df.at[idx, f'{exp_id}_mutation_score_%'] = result.get('mutation_score')
            df.at[idx, f'{exp_id}_total_mutants'] = result.get('total_mutants')
            df.at[idx, f'{exp_id}_killed_mutants'] = result.get('killed_mutants')
            df.at[idx, f'{exp_id}_survived_mutants'] = result.get('survived_mutants')

            # Timing & output
            df.at[idx, f'{exp_id}_duration_s'] = result.get('total_duration_seconds')
            df.at[idx, f'{exp_id}_tests_code'] = result.get('final_tests_code')
            df.at[idx, f'{exp_id}_cluster_info'] = result.get('cluster_details')
            df.at[idx, f'{exp_id}_error'] = result.get('error_message')

        # Save results
        output_file = output_path / f"{experiment_config.experiment_id}_results.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"Results saved to: {output_file}")

        # Save summary
        self._save_summary(df, experiment_config, output_path)

        return df

    async def _process_single_function(
            self,
            index: int,
            function_code: str,
            function_name: Optional[str],
            experiment_config: ExperimentConfig
    ) -> Dict[str, Any]:
        """Process a single function"""

        logger.info(f"Processing function {index}: {function_name or 'unnamed'}")

        try:
            # Build request
            request = TestGenerationRequest(
                function_code=function_code,
                function_name=function_name,
                clustering_method=experiment_config.clustering_method,
                eps=experiment_config.eps,
                min_samples=experiment_config.min_samples,
                models=experiment_config.models,
                roles=experiment_config.roles,
                enable_coverage=experiment_config.enable_coverage,
                enable_mutation=experiment_config.enable_mutation,
                stream_updates=False
            )

            # Generate tests
            response = await self.service.generate_tests_batch(
                request=request,
                experiment_config=experiment_config
            )

            # Extract cluster details
            cluster_info = [
                {
                    'cluster_id': c.cluster_id,
                    'size': c.size,
                    'category': c.category
                }
                for c in response.clusters
            ]

            # Extract quality metrics
            quality_metrics = response.coverage.quality_metrics if (response.coverage and response.coverage.quality_metrics) else {}

            # Extract mutation metrics
            mutation_results = response.coverage.mutation_results if (response.coverage and response.coverage.mutation_results) else {}

            result = {
                'index': index,
                'function_name': response.function_name,
                'experiment_id': experiment_config.experiment_id,
                'success': True,

                # ✅ Syntax validation
                'is_runnable': response.coverage.is_runnable if response.coverage else None,
                'syntax_error': response.coverage.syntax_error if response.coverage else None,

                'total_raw_tests': response.statistics.total_raw_tests,
                'total_clusters': response.statistics.total_clusters,
                'noise_tests': response.statistics.noise_tests,
                'final_tests_count': response.statistics.final_tests,

                # Coverage metrics (with new branch details)
                'coverage_percentage': response.coverage.coverage_percentage if response.coverage else None,
                'branch_coverage_percentage': response.coverage.branch_coverage_percentage if response.coverage else None,
                'total_branches': response.coverage.total_branches if response.coverage else None,        # ✅ NEW
                'covered_branches': response.coverage.covered_branches if response.coverage else None,    # ✅ NEW
                'has_branches': response.coverage.has_branches if response.coverage else None,            # ✅ NEW
                'passed_tests': response.coverage.passed_tests if response.coverage else None,
                'failed_tests': response.coverage.failed_tests if response.coverage else None,
                'success_rate': response.coverage.success_rate if response.coverage else None,

                # Quality metrics
                'assertion_density': quality_metrics.get('assertion_density'),
                'diversity_score': quality_metrics.get('diversity_score'),
                'edge_case_score': quality_metrics.get('edge_case_score'),
                'avg_test_complexity': quality_metrics.get('avg_test_complexity'),

                # Standard metrics
                'test_loc': quality_metrics.get('test_loc'),
                'source_loc': quality_metrics.get('source_loc'),
                'loc_efficiency': quality_metrics.get('loc_efficiency'),
                'duplication_rate': quality_metrics.get('duplication_rate'),
                'exception_coverage_rate': quality_metrics.get('exception_coverage_rate'),

                # Mutation metrics
                'mutation_score': mutation_results.get('mutation_score'),
                'total_mutants': mutation_results.get('total_mutants'),
                'killed_mutants': mutation_results.get('killed_mutants'),
                'survived_mutants': mutation_results.get('survived_mutants'),

                # Timing metrics
                'total_duration_seconds': response.statistics.total_duration_seconds,
                'llm_duration_seconds': response.statistics.llm_duration_seconds,
                'clustering_duration_seconds': response.statistics.clustering_duration_seconds,
                'synthesis_duration_seconds': response.statistics.synthesis_duration_seconds,
                'coverage_duration_seconds': response.statistics.coverage_duration_seconds,

                # Output
                'final_tests_code': response.final_tests,
                'cluster_details': json.dumps(cluster_info),
                'error_message': None
            }

            logger.info(f"✅ Function {index} completed successfully")
            return result

        except Exception as e:
            logger.error(f"❌ Function {index} failed: {e}", exc_info=True)
            return {
                'index': index,
                'function_name': function_name or 'unknown',
                'experiment_id': experiment_config.experiment_id,
                'success': False,
                'error_message': str(e),
                'is_runnable': None,
                'syntax_error': None,
                # Set all other metrics to None...
                'total_raw_tests': None,
                'total_clusters': None,
                'final_tests_count': None,
                'coverage_percentage': None,
                'branch_coverage_percentage': None,
                'total_branches': None,        # ✅ NEW
                'covered_branches': None,      # ✅ NEW
                'has_branches': None,          # ✅ NEW
                'passed_tests': None,
                'failed_tests': None,
                'success_rate': None,
                'assertion_density': None,
                'diversity_score': None,
                'edge_case_score': None,
                'avg_test_complexity': None,
                'test_loc': None,
                'source_loc': None,
                'loc_efficiency': None,
                'duplication_rate': None,
                'exception_coverage_rate': None,
                'mutation_score': None,
                'total_mutants': None,
                'killed_mutants': None,
                'survived_mutants': None,
                'total_duration_seconds': None,
                'final_tests_code': None,
                'cluster_details': None
            }

    def _save_summary(
            self,
            df: pd.DataFrame,
            experiment_config: ExperimentConfig,
            output_path: Path
    ):
        """Save experiment summary"""

        exp_id = experiment_config.experiment_id

        # Calculate statistics
        success_col = f'{exp_id}_success'
        total_funcs = len(df)
        successful = df[success_col].sum() if success_col in df.columns else 0
        failed = total_funcs - successful

        # ✅ Calculate syntax success rate
        runnable_col = f'{exp_id}_is_runnable'
        runnable_count = df[runnable_col].sum() if runnable_col in df.columns else 0
        runnable_rate = (runnable_count / total_funcs) * 100 if total_funcs > 0 else 0

        # ✅ Calculate branch coverage statistics
        has_branches_col = f'{exp_id}_has_branches'
        functions_with_branches = df[has_branches_col].sum() if has_branches_col in df.columns else 0

        # Average metrics (only successful runs)
        successful_df = df[df[success_col] == True] if success_col in df.columns else df

        avg_metrics = {}

        # Include all metrics (including new branch metrics)
        for metric in ['total_tests', 'clusters', 'final_tests',
                       'line_coverage_%', 'branch_coverage_%',
                       'total_branches', 'covered_branches',  # ✅ NEW
                       'passed_tests', 'failed_tests', 'test_success_rate_%',
                       'assertion_density', 'diversity_score', 'edge_case_score',
                       'avg_test_complexity',
                       'test_loc', 'source_loc', 'loc_efficiency',
                       'duplication_rate_%', 'exception_coverage_%',
                       'mutation_score_%', 'total_mutants', 'killed_mutants', 'survived_mutants',
                       'duration_s']:
            col = f'{exp_id}_{metric}'
            if col in successful_df.columns:
                avg_metrics[metric] = successful_df[col].mean()

        summary = {
            'experiment_id': experiment_config.experiment_id,
            'experiment_type': experiment_config.experiment_type.value,
            'description': experiment_config.description,
            'timestamp': datetime.utcnow().isoformat(),
            'total_functions': total_funcs,
            'successful': int(successful),
            'failed': int(failed),
            'success_rate': f"{(successful/total_funcs)*100:.1f}%",
            # ✅ Syntax validation statistics
            'runnable_tests': int(runnable_count),
            'runnable_rate': f"{runnable_rate:.1f}%",
            # ✅ NEW: Branch coverage statistics
            'functions_with_branches': int(functions_with_branches),
            'functions_with_branches_rate': f"{(functions_with_branches/total_funcs)*100:.1f}%",
            'average_metrics': avg_metrics,
            'config': experiment_config.dict()
        }

        # Save as JSON
        summary_file = output_path / f"{exp_id}_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)

        logger.info(f"\n{'='*60}")
        logger.info(f"EXPERIMENT SUMMARY: {exp_id}")
        logger.info(f"{'='*60}")
        logger.info(f"Summary saved to: {summary_file}")
        logger.info(f"Success rate: {summary['success_rate']}")
        # ✅ Log syntax validation rate
        logger.info(f"Runnable tests rate: {summary['runnable_rate']} ({int(runnable_count)}/{total_funcs})")
        # ✅ NEW: Log branch statistics
        logger.info(f"Functions with branches: {summary['functions_with_branches_rate']} ({int(functions_with_branches)}/{total_funcs})")

        # Log coverage metrics
        if 'line_coverage_%' in avg_metrics:
            logger.info(f"\n📊 COVERAGE METRICS:")
            logger.info(f"  Avg Line Coverage: {avg_metrics['line_coverage_%']:.2f}%")
        if 'branch_coverage_%' in avg_metrics:
            logger.info(f"  Avg Branch Coverage: {avg_metrics['branch_coverage_%']:.2f}%")
            # ✅ NEW: Log detailed branch statistics
            if 'total_branches' in avg_metrics:
                logger.info(f"  Avg Total Branches: {avg_metrics['total_branches']:.1f}")
            if 'covered_branches' in avg_metrics:
                logger.info(f"  Avg Covered Branches: {avg_metrics['covered_branches']:.1f}")

        # Log quality metrics
        logger.info(f"\n✨ QUALITY METRICS:")
        if 'assertion_density' in avg_metrics:
            logger.info(f"  Avg Assertion Density: {avg_metrics['assertion_density']:.2f}")
        if 'diversity_score' in avg_metrics:
            logger.info(f"  Avg Diversity Score: {avg_metrics['diversity_score']:.2f}/100")
        if 'edge_case_score' in avg_metrics:
            logger.info(f"  Avg Edge Case Score: {avg_metrics['edge_case_score']:.2f}/100")

        # Log standard metrics
        logger.info(f"\n📏 STANDARD METRICS:")
        if 'test_loc' in avg_metrics:
            logger.info(f"  Avg Test LOC: {avg_metrics['test_loc']:.1f}")
        if 'loc_efficiency' in avg_metrics:
            logger.info(f"  Avg LOC Efficiency: {avg_metrics['loc_efficiency']:.2f}")
        if 'duplication_rate_%' in avg_metrics:
            logger.info(f"  Avg Duplication Rate: {avg_metrics['duplication_rate_%']:.2f}%")
        if 'exception_coverage_%' in avg_metrics:
            logger.info(f"  Avg Exception Coverage: {avg_metrics['exception_coverage_%']:.2f}%")

        # ✅ Log mutation testing metrics
        if experiment_config.enable_mutation:
            logger.info(f"\n🧬 MUTATION TESTING (GOLD STANDARD):")
            if 'mutation_score_%' in avg_metrics:
                logger.info(f"  Avg Mutation Score: {avg_metrics['mutation_score_%']:.2f}%")
            if 'total_mutants' in avg_metrics:
                logger.info(f"  Avg Total Mutants: {avg_metrics['total_mutants']:.1f}")
            if 'killed_mutants' in avg_metrics:
                logger.info(f"  Avg Killed Mutants: {avg_metrics['killed_mutants']:.1f}")
            if 'survived_mutants' in avg_metrics:
                logger.info(f"  Avg Survived Mutants: {avg_metrics['survived_mutants']:.1f}")

        logger.info(f"{'='*60}\n")
