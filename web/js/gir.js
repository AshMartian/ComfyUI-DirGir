// web/js/gir.js

import { api } from '../../../scripts/api.js';
import { app } from '../../../scripts/app.js';

// console.log(app);

function getDirectoryPath(node_id) {
  return new Promise((resolve, reject) => {
  api.fetchApi('/gir-dir/select-directory?id=' + node_id)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        resolve(data.selected_folder);
    })
    .catch(error => {
        console.error('Error setting directory:', error);
    });
  });
}

function getCurrentDirectory(node_id) {
  return new Promise((resolve, reject) => {
  api.fetchApi('/gir-dir/get-directory?id=' + node_id)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        resolve(data.selected_folder);
    })
    .catch(error => {
        console.error('Error setting directory:', error);
        reject(error);
    });
  });
}

function setDirectoryPath(node_id, directory) {
  return new Promise((resolve, reject) => {
  api.fetchApi('/gir-dir/set-directory?id=' + node_id + '&directory=' + directory)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        resolve(data.status);
    })
    .catch(error => {
        console.error('Error setting directory:', error);
    });
  });
}

function getLoopIndex(node_id) {
  return new Promise((resolve, reject) => {
  api.fetchApi('/gir-dir/loop-index?id=' + node_id)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        resolve(data.loop_index);
    })
    .catch(error => {
        console.error('Error setting directory:', error);
        reject(error);
    });
  });
}

app.registerExtension({
  name: "DirGir.Picker",
  category: "Dir GIR",
  inputs: [{name: "Selected Directory", type: "string"}],
  outputs: [{name: "directory", type: "string"}],
  async beforeRegisterNodeDef (nodeType, nodeData, app) {
    if (nodeType.comfyClass == 'Dir_Gir_Picker') {
      const orig_nodeCreated = nodeType.prototype.onNodeCreated
      nodeType.prototype.onNodeCreated = async function () {
        await orig_nodeCreated?.apply(this, arguments)

        const node = this;

        var element = document.createElement("div");
        element.style.textOverflow = "ellipsis";
        element.style.fontSize = "12px";
        element.style.overflow = "hidden";
        element.style.whiteSpace = "break-word";
        element.style.width = "100%";
        element.style.fontFamily = "Arial, sans-serif";
        element.innerHTML = "No directory selected";
  
        const previewElement = node.addDOMWidget("directorypreview", "preview", element, {
          serialize: false,
          hideOnZoom: false,
          getValue() {
              return element.innerHTML;
          },
          setValue(v) {
              element.innerHTML = v;
          },
        });
        previewElement.computeSize = function() {
          return [200, 50];
        }
        node.widgets.filter(w => w.name === "Selected Directory").forEach(w => w.value = "");
        // Add a button widget to the node that opens a directory selection dialog
        node.addWidget("button", "Select Directory", null, function(widget) {
          getDirectoryPath(node.id).then(directory => {
            // Add a text element to the node that displays the selected directory
            element.innerHTML = directory;
            node.setOutputData("directory", directory);
            node.onResize?.(node.size);
            node.widgets.filter(w => w.name === "Selected Directory").forEach(w => w.value = directory);
          });
        });
  
        node.addWidget("text", "Selected Directory", "", function(widget) {
          setDirectoryPath(node.id, widget);
          element.innerHTML = widget;
        });
  
        getCurrentDirectory(node.id).then(directory => {
          if (directory) {
            element.innerHTML = directory;
            node.setOutputData("directory", directory);
            node.widgets.filter(w => w.name === "Selected Directory").forEach(w => w.value = directory);
          }
        });

      }
    }
  },
});

app.registerExtension({
  name: "DirGir.Looper",
  category: "Dir Gir",
  async beforeRegisterNodeDef (nodeType, nodeData, app) {
    if (nodeType.comfyClass == 'Dir_Gir_Looper') {
      const orig_nodeCreated = nodeType.prototype.onNodeCreated
      nodeType.prototype.onNodeCreated = async function () {
        await orig_nodeCreated?.apply(this, arguments)

        const node = this;

        getLoopIndex(node.id).then(loop_index => {
          node.widgets.find(w => w.name === 'loop_index').value = loop_index;
        });

        api.addEventListener('executed', async () => {
          getLoopIndex(node.id).then(loop_index => {
            node.widgets.find(w => w.name === 'loop_index').value = loop_index;
          });
        });
      }
    }
  },
});