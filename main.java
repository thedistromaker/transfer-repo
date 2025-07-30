import com.googlecode.lanterna.TerminalSize;
import com.googlecode.lanterna.TextColor;
import com.googlecode.lanterna.gui2.*;
import com.googlecode.lanterna.screen.*;
import com.googlecode.lanterna.terminal.DefaultTerminalFactory;

import java.util.Arrays;

public class TelemetryTUI {
    public static void main(String[] args) throws Exception {
        Screen screen = new DefaultTerminalFactory().createScreen();
        screen.startScreen();

        TerminalSize size = new TerminalSize(60, 10);
        WindowBasedTextGUI gui = new MultiWindowTextGUI(screen);
        BasicWindow window = new BasicWindow("Telemetry Monitor");

        Panel panel = new Panel();
        panel.setLayoutManager(new LinearLayout(Direction.VERTICAL));

        panel.addComponent(makeBar("Battery Voltage", 80));
        panel.addComponent(makeBar("Motor Temp", 60));
        panel.addComponent(makeBar("CPU Temp", 70));

        window.setComponent(panel);
        gui.addWindowAndWait(window);
    }

    private static Panel makeBar(String label, int percent) {
        Panel barPanel = new Panel(new LinearLayout(Direction.HORIZONTAL));
        barPanel.addComponent(new Label(label + ": "));
        StringBuilder bar = new StringBuilder();
        int blocks = percent / 5;
        for (int i = 0; i < 20; i++) {
            bar.append(i < blocks ? "#" : " ");
        }
        barPanel.addComponent(new Label("[" + bar + "] " + percent + "%"));
        return barPanel;
    }
}
