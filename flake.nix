{
  description = "SF6 Knowledge Agent Kit maintainer toolchain pins";

  inputs = {
    hermes-agent.url = "github:NousResearch/hermes-agent";
  };

  outputs = { self, hermes-agent }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
      ];
      forAllSystems = f:
        builtins.listToAttrs (map (system: {
          name = system;
          value = f system;
        }) systems);
    in
    {
      apps = forAllSystems (system: {
        default = {
          type = "app";
          program = "${hermes-agent.packages.${system}.default}/bin/hermes";
        };
        hermes = {
          type = "app";
          program = "${hermes-agent.packages.${system}.default}/bin/hermes";
        };
      });

      packages = forAllSystems (system: {
        default = hermes-agent.packages.${system}.default;
        hermes-agent = hermes-agent.packages.${system}.default;
      });
    };
}
