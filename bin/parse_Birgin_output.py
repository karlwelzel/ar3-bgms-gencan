import pathlib

import wandb


cwd = pathlib.Path.cwd()

for experiment_path in cwd.glob("experiments_p*/*_rmp.txt"):
    problem = experiment_path.stem.split("_")[0]
    p = experiment_path.parent.stem.split("_")[1][1]
    config = {
        "problem": problem,
        "p": p,
        "update_type": "Birgin",
        "update_decrease_measure": "TAYLOR",
        "update_sigma0": 1,
        "x0_type": "default",
        "stop_rule": "First_Order",
        "stop_tolerance_g": 1e-8,
        "inner_solver": "GENCAN",
        # "inner_stop_rule": "ARP_Theory",
        # "inner_stop_theta": 100,
        "inner_stop_rule": "First_Order",
        "inner_stop_tolerance_g": 1e-10,
    }
    wandb.init(project="ar3-project", group="birgin-code3", config=config)
    with open(experiment_path, "r") as file:
        print(experiment_path)
        for line in file.readlines():
            if not line:
                continue
            f, norm_g, norm_step, total_fun, total_der, total_solves, sigma, model_plus = line.split()
            wandb.log({
                "f": float(f),
                "norm_g": float(norm_g),
                "norm_step": float(norm_step),
                "total_fun": int(total_fun),
                "total_der": int(total_der),
                "total_solves": int(total_solves),
                "sigma": float(sigma),
                "model_plus": float(model_plus),
            })
    wandb.finish(quiet=True)
