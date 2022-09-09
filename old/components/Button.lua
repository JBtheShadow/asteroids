local love = require "love"
local Text = require "components.Text"

function Button(text, btn_x, btn_y, params)
    text = text or "No text"
    btn_x = btn_x or 0
    btn_y = btn_y or 0
    params = params or {}

    local func = params.func or function() print("No function attached to button '" .. text .. "'") end
    local text_color = params.text_color or { r = 1, g = 1, b = 1 }
    local hover_color = params.hover_color or { r = 0.8, g = 0.2, b = 0.2 }
    local btn_color = params.btn_color or { r = 0, g = 0, b = 0 }
    local width = params.width or 100
    local height = params.height or 50
    local text_align = params.text_align or "left"
    local font_size = params.font_size or "p"
    local text_x = params.text_x or 0
    local text_y = params.text_y or 0
    local btn_text = {
        x = text_x + btn_x,
        y = text_y + btn_y,
    }

    return {
        text_color = text_color,
        btn_color = btn_color,
        hover_color = hover_color,
        width = width,
        height = height,
        text = text,
        text_x = text_x,
        text_y = text_y,
        btn_x = btn_x,
        btn_y = btn_y,
        text_component = Text(text, btn_text.x, btn_text.y, {
            font_size = font_size,
            wrap_width = width,
            align = text_align,
        }),

        setBtnColor = function(self, red, green, blue)
            self.btn_color = { r = red, g = green, b = blue }
        end,

        setTextColor = function(self, red, green, blue)
            self.text_color = { r = red, g = green, b = blue }
        end,

        click = function(self) func() end,
        checkHover = function(self, mouse_x, mouse_y, cursor_radius)
            if mouse_x + cursor_radius >= self.btn_x and mouse_x - cursor_radius <= self.btn_x + self.width then
                if mouse_y + cursor_radius >= self.btn_y and mouse_y  - cursor_radius <= self.btn_y + self.height then
                    return true
                end
            end

            return false
        end,

        draw = function(self, mouse_x, mouse_y, cursor_radius)
            love.graphics.setColor(self.btn_color.r, self.btn_color.g, self.btn_color.b)
            love.graphics.rectangle("fill", self.btn_x, self.btn_y, self.width, self.height)

            if self:checkHover(mouse_x, mouse_y, cursor_radius) then
                self.text_component:setColor(self.hover_color.r, self.hover_color.g, self.hover_color.b)
            else
                self.text_component:setColor(self.text_color.r, self.text_color.g, self.text_color.b)
            end

            self.text_component:draw()

            love.graphics.setColor(1, 1, 1)
        end,

        getPos = function(self)
            return self.btn_x, self.btn_y
        end,

        getTextPos = function(self)
            return self.text_x, self.text_y
        end,
    }
end

return Button