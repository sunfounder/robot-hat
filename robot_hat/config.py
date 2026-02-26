import json
import os
from typing import Iterator, Any
from .basic import _Basic_class

class Config(_Basic_class):
    """ Config class

    Args:
        config_file (str): config file path
        *args: pass to :class:`#robot_hat._basic._Basic_class`
        **kwargs: pass to :class:`#robot_hat._basic._Basic_class`
    """
    def __init__(self, *args, config_file: str, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config_file = config_file
        
        if not os.path.exists(config_file):
            os.system(f'touch {config_file}')
            os.system(f'chown 1000:1000 {config_file}')
        with open(config_file, 'r') as f:
            content = f.read()
            if content == '':
                content = '{}'
            self._config = json.loads(content)

    def get(self, key: str, default_value: Any = None) -> Any:
        """ Get the value of the key

        Args:
            key (str): key name
            default_value (optional): default value if the key is not found. Defaults to None.

        Returns:
            Any: value of the key
        """
        return self._config.get(key, default_value)

    def set(self, key: str, value: Any) -> None:
        """ Set the value of the key

        Args:
            key (str): key name
            value (Any): value of the key
        """
        self._config[key] = value
        with open(self.config_file, 'w') as f:
            json.dump(self._config, f, indent=4)

    def delete(self, key: str) -> None:
        """ Delete the key

        Args:
            key (str): key name
        """
        if key in self._config:
            del self._config[key]
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=4)

    def __getitem__(self, key: str) -> Any:
        """
        Get the value of the key

        Args:
            key (str): key name

        Returns:
            Any: value of the key
        """
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """ Set the value of the key

        Args:
            key (str): key name
            value (Any): value of the key
        """
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        """ Delete the key

        Args:
            key (str): key name
        """
        self.delete(key)

    def __contains__(self, key: str) -> bool:
        """ Check if the key exists

        Args:
            key (str): key name

        Returns:
            bool: True if the key exists, False otherwise
        """
        return key in self._config

    def __iter__(self) -> Iterator[str]:
        """ Iterate over the keys

        Returns:
            Iterator[str]: iterator over the keys
        """
        return iter(self._config)

    def __len__(self) -> int:
        """ Get the number of keys

        Returns:
            int: number of keys
        """
        return len(self._config)

    def __str__(self) -> str:
        """ Get the string representation of the config

        Returns:
            str: string representation of the config
        """
        return json.dumps(self._config, indent=4)

    def __repr__(self) -> str:
        """ Get the string representation of the config

        Returns:
            str: string representation of the config
        """
        return f'Config({self.config_file})'
