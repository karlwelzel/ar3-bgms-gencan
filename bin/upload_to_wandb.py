import pathlib

import wandb


cwd = pathlib.Path.cwd()

for experiment_path in cwd.glob("experiments_p*/*_rmp.txt"):
    problem = experiment_path.stem.split("_")[0]
    p = experiment_path.parent.stem.split("_")[1][1]
    config = {
        "problem": problem,
        "p": int(p),
        "update_type": "BGMS",
        "update_use_prerejection": True,
        "update_sigma0": 1e-8,
        "x0_type": "default",
        "stop_rule": "First_Order",
        "stop_tolerance_g": 1e-8,
        "inner_solver": "GENCAN",
        # "inner_stop_rule": "ARP_Theory",
        # "inner_stop_theta": 100,
        "inner_stop_rule": "First_Order",
        "inner_stop_tolerance_g": 1e-9,
        "wandb_project": "ar3-project",
        "wandb_group": "Exp_Benchmark_3",
    }
    wandb.init(
        project=config["wandb_project"],
        group=config["wandb_group"],
        config=config,
    )
    with open(experiment_path, "r") as file:
        print(experiment_path)
        for line in file.readlines():
            if not line:
                continue
            (
                f,
                norm_g,
                norm_step,
                total_fun,
                total_der,
                total_solves,
                sigma,
                model_plus,
                geninfo,
            ) = line.split()
            sub_status = {
                -1: float("nan"),  # no subproblem solve
                0: 0,  # SUCCESS
                1: -1,  # MAX_ITERATIONS_EXCEEDED
                3: -2,  # NUMERICAL_ISSUES
                6: -4,  # NOT_LOWER_BOUNDED
            }[int(geninfo)]
            wandb.log(
                {
                    "f": float(f),
                    "norm_g": float(norm_g),
                    "norm_step": float(norm_step),
                    "total_fun": int(total_fun),
                    "total_der": int(total_der),
                    "total_solves": int(total_solves),
                    "sigma": float(sigma),
                    # "model_plus": float(model_plus),
                    "sub_status": sub_status,
                }
            )
    wandb.finish(quiet=True)

    experiment_path.unlink()
