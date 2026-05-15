extends Node
## Background music controller (Autoload). Loops a track and crossfades
## between the sailing theme and the in-port theme.

const TRACKS := {
	"sea": "res://assets/audio/bgm_sea.ogg",
	"port": "res://assets/audio/bgm_port.ogg",
}
const BGM_DB := -9.0

var _player: AudioStreamPlayer
var _current: String = ""
var _muted: bool = false


func _ready() -> void:
	_player = AudioStreamPlayer.new()
	_player.volume_db = BGM_DB
	add_child(_player)


func play(track: String) -> void:
	if track == _current or not TRACKS.has(track):
		return
	_current = track
	var stream: AudioStream = load(TRACKS[track])
	if stream is AudioStreamOggVorbis:
		stream.loop = true
	_player.stream = stream
	_player.play()


func toggle_mute() -> bool:
	_muted = not _muted
	_player.volume_db = -80.0 if _muted else BGM_DB
	return _muted
