import { DefaultPluginSpec } from "/static/mol-plugin/spec.js"
import { PluginContext } from "/static/mol-plugin/context.js"

export async function initViewer(element, options) {
  const parent =
    typeof element === "string" ? document.getElementById(element) : element
  const canvas = document.createElement("canvas")
  parent.appendChild(canvas)

  const spec = options?.spec ?? DefaultPluginSpec()

  const plugin = new PluginContext(spec)
  await plugin.init()

  plugin.initViewer(canvas, parent)

  return plugin
}

export async function loadStructure(plugin, url, options) {
  const data = await plugin.builders.data.download({
    url,
    isBinary: options?.isBinary
  })
  const trajectory = await plugin.builders.structure.parseTrajectory(
    data,
    options?.format ?? "mmcif"
  )
  const preset = await plugin.builders.structure.hierarchy.applyPreset(
    trajectory,
    "default"
  )
  return preset
}