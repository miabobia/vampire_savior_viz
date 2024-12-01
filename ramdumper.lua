for _,var in ipairs({playbackfile, use_last_recording,
					path,playkey,recordkey,togglepausekey,toggleloopkey,longwait,longpress,longline,framemame, show_position,
					 display_recording_gui,
					 use_hb_config, hb_config_blank_screen, hb_config_draw_axis, hb_config_draw_pushboxes, hb_config_draw_throwable_boxes, hb_config_no_alpha,
					 mo_enable_frame_data, debug, quiet_framedata, show_controls_message}) do
	var = nil
end

function script_path()
	local str = debug.getinfo(2, "S").source:sub(2)
	return str:match("(.*[/\\])")
end
function deepcopy(orig)
    local orig_type = type(orig)
    local copy
    if orig_type == 'table' then
        copy = {}
        for orig_key, orig_value in next, orig, nil do
            copy[deepcopy(orig_key)] = deepcopy(orig_value)
        end
        setmetatable(copy, deepcopy(getmetatable(orig)))
    else -- number, string, boolean, etc
        copy = orig
    end
    return copy
end
copytable = deepcopy
dofile("macro-options.lua", "r") --load the globals
dofile("macro-modules.lua", "r")

serialize                = require './scripts/ser'
local json               = require './scripts/dkjson'

local p1_addr = 0xFF8400
local p2_addr = 0xFF8800

emu.registerstart(function()
end)

function write_object_to_json_file(_object, _file_path)
	-- print(serialize(_object))
	local start_clock = os.time(os.date("!*t"))
	-- print("Opening at", start_clock)

	local _f = io.open(_file_path, "w")
	if _f == nil then
	  return false
	end
  
	local _str = json.encode(_object, { indent = false })
	_f:write("\r\n")
	_f:write(_str)

	_f:flush()
	_f:close()
	local end_clock = os.time(os.date("!*t"))
	-- print("closing at", end_clock - start_clock)

	return true
end

local last 
emu.registerbefore(function()
    memory.writeword(0xFF8000 + 0x109, 0x64 )

    local p1_values = {}
	local p2_values = {}
    -- A byte is just 1!
    for i=0, 0x200, 1 do
        local address = 0xFF8400 + i
        local value = memory.readbyte(address)
        p1_values[address] = value
        -- p1_values["framecount"] = emu.framecount()
    end
    for i=0, 0x200, 1 do
        local address = 0xFF8800 + i
        local value = memory.readbyte(address)
        p2_values[address] = value
        -- p1_values["framecount"] = emu.framecount()
    end
	local all_values = {p1 = p1_values, p2 = p2_values}
    write_object_to_json_file(all_values, "./test_ram_dumper_state_dump.json")

end)

----------------------------------------------------------------------------------------------------
--[[ Handle pausing in the while true loop. ]]--
while true do
	gui.register(function()
	end)

    if pausenow then
        emu.pause()
        pausenow = false
    end
    emu.frameadvance()

	amountOfGarbage = collectgarbage("count")
	if amountOfGarbage > 15000 then
		collectgarbage("collect")
	end
end
