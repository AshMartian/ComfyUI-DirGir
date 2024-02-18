// web/js/gir.js

import { api } from '../../../scripts/api.js';
import { app } from '../../../scripts/app.js';

// console.log(app);

function getDirectoryPath(node_id) {
  return new Promise((resolve, reject) => {
  api.fetchApi('/select-directory?id=' + node_id)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Directory set successfully:', data);
        resolve(data.selected_folder);
        // Here you can use `data` to update the node or UI as needed
    })
    .catch(error => {
        console.error('Error setting directory:', error);
    });
  });
}

function getCurrentDirectory(node_id) {
  return new Promise((resolve, reject) => {
  api.fetchApi('/get-directory?id=' + node_id)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Directory got successfully:', data);
        resolve(data.selected_folder);
        // Here you can use `data` to update the node or UI as needed
    })
    .catch(error => {
        console.error('Error setting directory:', error);
        reject(error);
    });
  });
}

function setDirectoryPath(node_id, directory) {
  return new Promise((resolve, reject) => {
  api.fetchApi('/set-directory?id=' + node_id + '&directory=' + directory)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Directory set successfully:', data);
        resolve(data.status);
        // Here you can use `data` to update the node or UI as needed
    })
    .catch(error => {
        console.error('Error setting directory:', error);
    });
  });
}

app.registerExtension({
  name: "DirGir.DirPicker",
  category: "Dir Gir",
  inputs: [{name: "Selected Directory", type: "string"}],
  outputs: [{name: "directory", type: "string"}],
  loadedGraphNode: function(node) {
    console.log(node.comfyClass, node)
    if(node.comfyClass === "Dir_Gir_DirPicker") {
      var element = document.createElement("div");
      // Set height to 20px
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
});