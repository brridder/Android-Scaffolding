package <PACKAGE>;

import android.app.ListActivity;
import android.os.Bundle;
import android.widget.BaseAdapter;

import <PACKAGE>.R;

public class <CLASS_NAME> extends ListActivity {

    BaseAdapter mAdapter;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.<LAYOUT_CLASS_NAME>);

    }        

}
