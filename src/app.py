import argparse

def build_parser() -> argparse.ArgumentParser:
    """Builds the command line parser
    Returns: An argument parser ready to parse arguments for this program

    """
    parser = argparse.ArgumentParser(
        description="CLI interface for the CASTLE algorithm."
    )

    parser.add_argument(
        "--k",
        nargs="?",
        type=int,
        help="The value of k-anonymity to use"
    )

    parser.add_argument(
        "--delta",
        nargs="?",
        type=int,
        help="The maximum number of tuples to store before outputting"
    )

    parser.add_argument(
        "--beta",
        nargs="?",
        type=int,
        help="The maximum number of clusters to allow"
    )

    parser.add_argument(
        "--mu",
        nargs="?",
        type=int,
        help="The number of most recent loss values to use for tau"
    )

    parser.add_argument(
        "--l",
        nargs="?",
        type=int,
        help="The value of l to use"
    )
    
    """NEW T_kc"""
    parser.add_argument(
        "--tkc",
        nargs="?",
        type=int,
        help="The value of anonymized clusters to save and use for cluster selection"
    )
    
    """NEW year"""
    parser.add_argument(
        "--year",
        nargs="?",
        type=str,
        help="The year of the dataset to use"
    )
    
    """NEW month"""
    parser.add_argument(
        "--month",
        nargs="?",
        type=str,
        help="The month of the dataset to use"
    )
    
    """NEW n_users"""
    parser.add_argument(
        "--n_users",
        nargs="?",
        type=int,
        help="The number of users to use from data set"
    )
    
    """NEW user_id"""
    parser.add_argument(
        "--user_id",
        nargs="?",
        type=int,
        help="The ID of the user to use in case of only 1 user"
    )

    parser.add_argument(
        "--seed",
        type=int,
        help="The random seed to use for the simulation"
    )

    parser.add_argument(
        "--sample-size",
        nargs="?",
        default=20,
        type=int,
        help="The number of samples to use for the simulation"
    )

    parser.add_argument(
        "-f", "--filename",
        nargs="?",
        default="data.csv",
        type=str,
        help="The filepath to read data from"
    )

    parser.add_argument(
        "--display",
        action="store_true",
        help="Whether or not to display a graph after execution"
    )

    parser.add_argument(
        "--disable-dp",
        action="store_false",
        help="Whether or not to disable differential privacy"
    )

    parser.add_argument(
        "--phi",
        nargs="?",
        type=int,
        help="The phi value used to perturb tuples for differential privacy"
    )

    parser.add_argument(
        "--big-beta",
        nargs="?",
        type=float,
        help="Drop input tuples with probability 1 - beta"
    )

    parser.add_argument(
        "--history",
        action="store_true",
        help="Whether or not to store a history of all inserted tuples"
    )
    
    return parser

def parse_args() -> argparse.Namespace:
    """Parses the arguments specified on the command line
    Returns: The arguments that were specified on the command line and parsed
    by the object returned by build_parser()

    """
    parser = build_parser()
    return parser.parse_args()
