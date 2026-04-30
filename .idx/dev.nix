{ pkgs }:
{
  packages = [
    pkgs.python3
    pkgs.python3Packages.flask
    pkgs.python3Packages.flask-sqlalchemy
    pkgs.python3Packages.gunicorn
    pkgs.python3Packages.werkzeug
  ];
}