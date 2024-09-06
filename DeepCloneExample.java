import java.util.Map;
import java.util.HashMap;
import java.util.stream.Collectors;

// Assuming this is your TemplateDataItem class
class TemplateDataItem {
    private String value;
    private String jsonSubtype;

    public TemplateDataItem(String value, String jsonSubtype) {
        this.value = value;
        this.jsonSubtype = jsonSubtype;
    }

    // Copy constructor for deep cloning
    public TemplateDataItem(TemplateDataItem item) {
        this.value = item.value;
        this.jsonSubtype = item.jsonSubtype;
    }

    public String getValue() {
        return value;
    }

    public String getJsonSubtype() {
        return jsonSubtype;
    }

    @Override
    public String toString() {
        return "TemplateDataItem{" +
                "value='" + value + '\'' +
                ", jsonSubtype='" + jsonSubtype + '\'' +
                '}';
    }
}

public class DeepCloneExample {
    public static void main(String[] args) {
        // Original map
        Map<String, Map<String, TemplateDataItem>> originalMap = new HashMap<>();
        Map<String, TemplateDataItem> innerMap = new HashMap<>();
        innerMap.put("item1", new TemplateDataItem("value1", "jsonSubtype1"));
        originalMap.put("key1", innerMap);

        // Deep clone using streams
        Map<String, Map<String, TemplateDataItem>> clonedMap = originalMap.entrySet().stream()
            .collect(Collectors.toMap(
                Map.Entry::getKey,
                outerEntry -> outerEntry.getValue().entrySet().stream()
                    .collect(Collectors.toMap(
                        Map.Entry::getKey,
                        innerEntry -> new TemplateDataItem(innerEntry.getValue()) // Deep copy of TemplateDataItem
                    ))
            ));

        // Display cloned map to verify
        System.out.println("Original Map: " + originalMap);
        System.out.println("Cloned Map: " + clonedMap);
    }
}
