# System prompt:

You are a helpful programming assistant, who specializes in CI & CD.

# User prompt:

My github action is failing with the errors:
```
Run # Use '--skip-pkg-install' to prevent package re-installation 
  
.tox create: /home/runner/work/babylon_oracle/babylon_oracle/.tox/.tox
.tox installdeps: tox >= 4.0
lint: recreate env because requirements removed: pylint -e .
lint: remove tox env folder /home/runner/work/babylon_oracle/babylon_oracle/.tox/lint
.pkg: install_requires> python -I -m pip install poetry 'poetry-core>=1.0.0' tox-poetry
.pkg: _optional_hooks> python /home/runner/work/babylon_oracle/babylon_oracle/.tox/.tox/lib/python3.13/site-packages/pyproject_api/_backend.py True poetry.core.masonry.api
.pkg: get_requires_for_build_sdist> python /home/runner/work/babylon_oracle/babylon_oracle/.tox/.tox/lib/python3.13/site-packages/pyproject_api/_backend.py True poetry.core.masonry.api
.pkg: get_requires_for_build_wheel> python /home/runner/work/babylon_oracle/babylon_oracle/.tox/.tox/lib/python3.13/site-packages/pyproject_api/_backend.py True poetry.core.masonry.api
.pkg: freeze> python -m pip freeze --all
.pkg: anyio==4.11.0,build==1.3.0,CacheControl==0.14.3,certifi==2025.10.5,cffi==2.0.0,charset-normalizer==3.4.4,cleo==2.1.0,crashtest==0.4.1,cryptography==46.0.3,distlib==0.4.0,dulwich==0.24.7,fastjsonschema==2.21.2,filelock==3.20.0,findpython==0.7.0,h11==0.16.0,httpcore==1.0.9,httpx==0.28.1,idna==3.11,installer==0.7.0,jaraco.classes==3.4.0,jaraco.context==6.0.1,jaraco.functools==4.3.0,jeepney==0.9.0,keyring==25.6.0,more-itertools==10.8.0,msgpack==1.1.2,packaging==25.0,pbs-installer==2025.10.14,pip==25.2,pkginfo==1.12.1.2,platformdirs==4.5.0,pluggy==1.6.0,poetry==2.2.1,poetry-core==2.2.1,py==1.11.0,pycparser==2.23,pyproject_hooks==1.2.0,RapidFuzz==3.14.1,requests==2.32.5,requests-toolbelt==1.0.0,SecretStorage==3.4.0,shellingham==1.5.4,six==1.17.0,sniffio==1.3.1,toml==0.10.2,tomlkit==0.13.3,tox==3.28.0,tox-poetry==0.5.0,trove-classifiers==2025.9.11.17,urllib3==2.5.0,virtualenv==20.35.3,zstandard==0.25.0
.pkg: prepare_metadata_for_build_wheel> python /home/runner/work/babylon_oracle/babylon_oracle/.tox/.tox/lib/python3.13/site-packages/pyproject_api/_backend.py True poetry.core.masonry.api
.pkg: build_sdist> python /home/runner/work/babylon_oracle/babylon_oracle/.tox/.tox/lib/python3.13/site-packages/pyproject_api/_backend.py True poetry.core.masonry.api
lint: install_package_deps> python -I -m pip install 'Flask-Cors<5.0.0,>=4.0.1' 'connexion[flask,swagger-ui,uvicorn]<4.0.0,>=3.2.0' hvac==2.3.0 'pydantic<3.0.0,>=2.12.3' 'python-dotenv<2.0.0,>=1.1.1' 'requests<3.0.0,>=2.32.5'
lint: install_package> python -I -m pip install --force-reinstall --no-deps /home/runner/work/babylon_oracle/babylon_oracle/.tox/.tmp/package/1/oracle_server-0.1.0.tar.gz
lint: commands[0]> pylint --rc-file=.pylintrc oracle_server/
************* Module oracle_server.mcp_server
oracle_server/mcp_server.py:5:0: E0401: Unable to import 'pydantic' (import-error)
************* Module oracle_server.health
oracle_server/health.py:5:0: E0401: Unable to import 'flask' (import-error)
************* Module oracle_server.app
oracle_server/app.py:10:0: E0401: Unable to import 'connexion' (import-error)
oracle_server/app.py:11:0: E0401: Unable to import 'werkzeug.exceptions' (import-error)
oracle_server/app.py:13:0: E0401: Unable to import 'flask' (import-error)
oracle_server/app.py:14:0: E0401: Unable to import 'flask_cors' (import-error)
************* Module oracle_server.config.hashicorp
oracle_server/config/hashicorp.py:6:0: E0401: Unable to import 'hvac' (import-error)
-----------------------------------
Your code has been rated at 8.87/10
lint: exit 2 (4.20 seconds) /home/runner/work/babylon_oracle/babylon_oracle> pylint --rc-file=.pylintrc oracle_server/ pid=2538
lint: FAIL ✖ in 21.93 seconds
format: recreate env because requirements removed: black
format: remove tox env folder /home/runner/work/babylon_oracle/babylon_oracle/.tox/format
format: install_package_deps> python -I -m pip install 'Flask-Cors<5.0.0,>=4.0.1' 'connexion[flask,swagger-ui,uvicorn]<4.0.0,>=3.2.0' hvac==2.3.0 'pydantic<3.0.0,>=2.12.3' 'python-dotenv<2.0.0,>=1.1.1' 'requests<3.0.0,>=2.32.5'
format: install_package> python -I -m pip install --force-reinstall --no-deps /home/runner/work/babylon_oracle/babylon_oracle/.tox/.tmp/package/2/oracle_server-0.1.0.tar.gz
format: commands[0]> black oracle_server --check --diff
All done! ✨ 🍰 ✨
15 files would be left unchanged.
format: OK ✔ in 10.92 seconds
pytest: recreate env because requirements removed: flask_cors pytest -e . flask
pytest: remove tox env folder /home/runner/work/babylon_oracle/babylon_oracle/.tox/pytest
pytest: install_package_deps> python -I -m pip install 'Flask-Cors<5.0.0,>=4.0.1' 'connexion[flask,swagger-ui,uvicorn]<4.0.0,>=3.2.0' hvac==2.3.0 'pydantic<3.0.0,>=2.12.3' 'python-dotenv<2.0.0,>=1.1.1' 'requests<3.0.0,>=2.32.5'
pytest: install_package> python -I -m pip install --force-reinstall --no-deps /home/runner/work/babylon_oracle/babylon_oracle/.tox/.tmp/package/3/oracle_server-0.1.0.tar.gz
pytest: commands[0]> pytest tests
ImportError while loading conftest '/home/runner/work/babylon_oracle/babylon_oracle/tests/conftest.py'.
tests/conftest.py:6: in <module>
    from oracle_server.config.hashicorp import OpenBaoApiClient, BaoSecretsManager
oracle_server/config/hashicorp.py:6: in <module>
    import hvac
E   ModuleNotFoundError: No module named 'hvac'
pytest: exit 4 (0.79 seconds) /home/runner/work/babylon_oracle/babylon_oracle> pytest tests pid=2769
.pkg: _exit> python /home/runner/work/babylon_oracle/babylon_oracle/.tox/.tox/lib/python3.13/site-packages/pyproject_api/_backend.py True poetry.core.masonry.api
  lint: FAIL code 2 (21.93=setup[17.73]+cmd[4.20] seconds)
  format: OK (10.92=setup[10.43]+cmd[0.49] seconds)
  pytest: FAIL code 4 (11.22=setup[10.43]+cmd[0.79] seconds)
  evaluation failed :( (44.09 seconds)
Error: Process completed with exit code 255.
```

The action is defined in `.github/workflows/babylon-mcp-server.yml`

The actions use tox, as defined by `tox.ini`.

Poetry is used for dependency management. See `pyproject.yml`.

## Allowed Actions:
- `poetry`
- `tox`
