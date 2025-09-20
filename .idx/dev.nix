# dev.nix
{ pkgs, ... }: {
  channel = "stable-24.05";

  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.git
  ];

  env = {
    PORT = "8000"; # fallback if $PORT is not set
  };

  idx = {
    extensions = [];

    previews = {
      enable = true;
      previews = {
        web = {
          command = ["./devserver.sh"];
          manager = "web";
          env = {
            PORT = "$PORT";
          };
        };
      };
    };

    workspace = {
      onCreate = {
        install-requirements = ''
          echo "Installing Python dependencies..."
          python -m venv venv
          source venv/bin/activate
          pip install --upgrade pip
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          else
            pip install django
          fi

          chmod +x devserver.sh
        '';
      };

      onStart = {
        ensure-deps = ''
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          fi
        '';
      };
    };
  };
}
