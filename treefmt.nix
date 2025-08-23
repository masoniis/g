{ ... }:
{
  projectRootFile = "flake.nix";
  programs = {
    ruff.enable = true;
    nixfmt.enable = true;
    prettier.enable = true;
    clang-format.enable = true;
  };
}
