local love = require "love"

---Text component to be used in the game.
---@param text string Text to be displayed
---@param x number x position of text
---@param y number y position of text
---@param params table Additional parameters
---    -> font_size: string
---        -> default: "p"
---        -> options: "h1" through "h6", "p"
---    -> fade_in: boolean -- Should the text fade in
---        -> default: false
---    -> fade_out: boolean -- Should the text fade out
---        -> default: false
---    -> wrap_width: number -- When should text wrap around
---        -> default: love.graphics.getWidth()
---    -> align: string -- Align text to location
---        -> default: "left"
---        -> options: "left", "center", "right"
---    -> opacity: number
---        -> default: 1
---        -> options: 0.1 to 1
---        -> -- Setting fade_in to true will overwrite opacity to 0.1
---@return table
function Text(text, x, y, params)
    local font_size = params and params.font_size or "p"
    local fade_in = params and params.fade_in or false
    local fade_out = params and params.fade_out or false
    local wrap_width = params and params.wrap_width or love.graphics.getWidth()
    local align = params and params.align or "left"
    local opacity = params and params.opacity or 1

    local TEXT_FADE_DUR = 5
    local fonts = {
        h1 = love.graphics.newFont(60),
        h2 = love.graphics.newFont(50),
        h3 = love.graphics.newFont(40),
        h4 = love.graphics.newFont(30),
        h5 = love.graphics.newFont(20),
        h6 = love.graphics.newFont(10),
        p = love.graphics.newFont(16)
    }

    if fade_in then
        opacity = 0.1
    end

    return {
        text = text,
        x = x,
        y = y,
        opacity = opacity,

        colors = { r = 1, g = 1, b = 1 },
        setColor = function(self, red, green, blue)
            self.colors.r, self.colors.g, self.colors.b = red, green, blue
        end,

        draw = function(self, tbl_text, index)
            if self.opacity > 0 then
                if fade_in then
                    if self.opacity < 1 then
                        self.opacity = self.opacity + 1 / TEXT_FADE_DUR / love.timer.getDelta()
                    else
                        fade_in = false
                    end
                elseif fade_out then
                    self.opacity = self.opacity - 1 / TEXT_FADE_DUR / love.timer.getDelta()
                end

                love.graphics.setColor(self.colors.r, self.colors.g, self.colors.b, self.opacity)
                love.graphics.setFont(fonts[font_size])
                love.graphics.printf(self.text, self.x, self.y, wrap_width, align)
                love.graphics.setFont(fonts["p"])
            else
                table.remove(tbl_text, index)
                return false
            end

            return true
        end,
    }
end

return Text