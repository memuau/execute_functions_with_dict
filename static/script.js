function updateContent(methodData) {
  document.getElementById("methodData").innerHTML = new FunctionData(
    methodData
  ).Render();
}


class FunctionData {
  constructor(methodData) {
    this.methodData = methodData;
  }
  Render() {
    return `
        <h1>${this.methodData.name}</h1>
        <h2>Docs</h2>
        ${this.methodData.docs}
        <h2>Parameters</h2>
        ${this.createFormWithParams()}  
        `
  }
  createFormWithParams() {
    let result = `<form action= "executeCommand" method="POST">`
    result += "<h3>Mandatory</h3>"
    for (const [paramName, paramType] of Object.entries(this.methodData.params.mandatory)) {
        result += `<label for="${paramName}">${paramName}: <b>${paramType}</b></label>`
        result += `<input type="text" name="${paramName}" value= ""><br><br>`
    }
    result = result.slice(0, -4)
    result += "<h3>Optional</h3>"
    for (const [paramName, paramType] of Object.entries(this.methodData.params.optional)) {
        result += `<label for="${paramName}">${paramName}: <b>${paramType}</b></label>`
        result += `<input type="text" name="${paramName}" value= ""><br><br>`
    }
    if (result.endsWith("<h3>Optional</h3>") == true){
      result = result.slice(0, -17)
    }
    result += `<input type="hidden" name="function" id="function" value="${this.methodData.name}" />`
    result += `<input id="submit" type="submit" value="Execute command">`
    return result
  }
}
