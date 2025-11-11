#!/usr/bin/env python3
"""
Batch Experiment Runner
Run all 5 experiments on a CSV of Python functions
"""

import argparse
import asyncio
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DATA_DIR = PROJECT_ROOT / "app" / "data"
INPUT_DIR = DATA_DIR / "input"
RESULTS_DIR = DATA_DIR / "results"

# Add project root to path
sys.path.insert(0, str(PROJECT_ROOT))

from loguru import logger
from app.models.experiments import get_experiment_configs
from app.core.services.batch_testing_service import BatchTestingService


async def run_all_experiments(
        csv_filename: str,  # ✅ Changed from csv_path to csv_filename
        max_concurrent: int = 3
):
    """Run all 5 experiments on the CSV"""

    # ✅ Construct full paths
    csv_path = INPUT_DIR / csv_filename
    output_dir = RESULTS_DIR

    # ✅ Ensure directories exist
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("="*60)
    logger.info("BATCH EXPERIMENT RUNNER")
    logger.info("="*60)
    logger.info(f"Project Root: {PROJECT_ROOT}")
    logger.info(f"Input CSV: {csv_path}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Max concurrent: {max_concurrent}")

    # ✅ Validate CSV exists
    if not csv_path.exists():
        logger.error(f"Input CSV not found: {csv_path}")
        logger.info(f"Please place your CSV file in: {INPUT_DIR}")
        return

    # Get all experiment configs
    experiments = get_experiment_configs()

    logger.info(f"\nRunning {len(experiments)} experiments:")
    for exp in experiments:
        logger.info(f"  - {exp.experiment_id}: {exp.description}")

    # Create service
    service = BatchTestingService()

    # Run each experiment
    results = {}
    for i, exp_config in enumerate(experiments, 1):
        logger.info("\n" + "="*60)
        logger.info(f"EXPERIMENT {i}/{len(experiments)}: {exp_config.experiment_id}")
        logger.info(f"Description: {exp_config.description}")
        logger.info("="*60)

        try:
            df = await service.process_csv_batch(
                csv_path=str(csv_path),
                experiment_config=exp_config,
                output_dir=str(output_dir),
                max_concurrent=max_concurrent
            )
            results[exp_config.experiment_id] = {
                'success': True,
                'dataframe': df
            }
            logger.info(f"✅ Experiment {exp_config.experiment_id} completed successfully")

        except Exception as e:
            logger.error(f"❌ Experiment {exp_config.experiment_id} failed: {e}", exc_info=True)
            results[exp_config.experiment_id] = {
                'success': False,
                'error': str(e)
            }

    # Final summary
    logger.info("\n" + "="*60)
    logger.info("ALL EXPERIMENTS COMPLETE")
    logger.info("="*60)

    successful = sum(1 for r in results.values() if r['success'])
    logger.info(f"Successful: {successful}/{len(experiments)}")

    for exp_id, result in results.items():
        status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
        logger.info(f"{status}: {exp_id}")
        if not result['success']:
            logger.error(f"  Error: {result.get('error')}")

    logger.info(f"\nResults saved to: {output_dir}")


async def run_single_experiment(
        csv_filename: str,  # ✅ Changed from csv_path
        experiment_id: str,
        max_concurrent: int = 3
):
    """Run a single experiment"""

    # ✅ Construct full paths
    csv_path = INPUT_DIR / csv_filename
    output_dir = RESULTS_DIR

    # ✅ Ensure directories exist
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    logger.info(f"Running single experiment: {experiment_id}")
    logger.info(f"Input CSV: {csv_path}")
    logger.info(f"Output directory: {output_dir}")

    # ✅ Validate CSV exists
    if not csv_path.exists():
        logger.error(f"Input CSV not found: {csv_path}")
        logger.info(f"Please place your CSV file in: {INPUT_DIR}")
        return

    # Get experiment config
    all_experiments = {exp.experiment_id: exp for exp in get_experiment_configs()}

    if experiment_id not in all_experiments:
        logger.error(f"Invalid experiment ID: {experiment_id}")
        logger.info(f"Available experiments: {list(all_experiments.keys())}")
        return

    exp_config = all_experiments[experiment_id]

    # Create service and run
    service = BatchTestingService()

    try:
        df = await service.process_csv_batch(
            csv_path=str(csv_path),  # ✅ Convert Path to string
            experiment_config=exp_config,
            output_dir=str(output_dir),  # ✅ Convert Path to string
            max_concurrent=max_concurrent
        )
        logger.info(f"✅ Experiment completed successfully")
        logger.info(f"Results saved to: {output_dir}")

    except Exception as e:
        logger.error(f"❌ Experiment failed: {e}", exc_info=True)


def main():
    parser = argparse.ArgumentParser(
        description="Run batch test generation experiments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  # Run all 5 experiments (CSV should be in app/data/input/)
  python app/scripts/run_batch_experiments.py --csv functions.csv

  # Run single experiment
  python app/scripts/run_batch_experiments.py --csv functions.csv --experiment exp_1_full_system

  # Increase concurrency
  python app/scripts/run_batch_experiments.py --csv functions.csv --concurrent 5

Directory Structure:
  Input CSV:  {INPUT_DIR}/
  Results:    {RESULTS_DIR}/

Available Experiments:
  exp_1_full_system      - Full system (baseline)
  exp_2_no_roles         - Ablation 1: No role personas
  exp_3_single_model     - Ablation 2: Single model only
  exp_4_no_clustering    - Ablation 3: No clustering
  exp_5_no_synthesis     - Ablation 4: No synthesis
        """
    )

    parser.add_argument(
        '--csv',
        required=True,
        help='CSV filename (must be in app/data/input/ directory)',
        metavar='FILENAME'
    )

    parser.add_argument(
        '--experiment',
        help='Run specific experiment (default: run all)',
        choices=[
            'exp_1_full_system',
            'exp_2_no_roles',
            'exp_3_single_model',
            'exp_4_no_clustering',
            'exp_5_no_synthesis'
        ]
    )

    parser.add_argument(
        '--concurrent',
        type=int,
        default=3,
        help='Max concurrent function processing (default: 3)'
    )

    args = parser.parse_args()

    # Run experiments
    if args.experiment:
        asyncio.run(run_single_experiment(
            csv_filename=args.csv,
            experiment_id=args.experiment,
            max_concurrent=args.concurrent
        ))
    else:
        asyncio.run(run_all_experiments(
            csv_filename=args.csv,
            max_concurrent=args.concurrent
        ))


if __name__ == '__main__':
    main()
