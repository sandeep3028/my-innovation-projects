import requests


def set_lights(light_id, payload):
    hue_url = f'http://192.168.0.148/api/TqbzJd6ewt2TSllQZKzDFJQeuhP8HHESdLZgfWKh/lights/{light_id}/state'
    requests.put(hue_url, json=payload)
